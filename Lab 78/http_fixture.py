import threading
import time
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse


@contextmanager
def local_site(delay=0.03):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            path = urlparse(self.path).path
            status = 200
            if path.startswith("/delay/"):
                time.sleep(float(path.rsplit("/", 1)[1]))
            elif path == "/slow":
                time.sleep(0.2)
            else:
                time.sleep(delay)
            if path == "/flaky":
                with self.server.counter_lock:
                    self.server.flaky_count += 1
                    status = 503 if self.server.flaky_count == 1 else 200
            elif path.startswith("/status/"):
                status = int(path.rsplit("/", 1)[1])
            body = (
                f"<html><head><title>Fixture {path}</title></head><body>"
                "<h1>Local lab fixture</h1><p>First paragraph.</p>"
                "<p>Second paragraph.</p><a href='/next'>Next</a>"
                "<a href='/empty'></a><img src='/image.png'></body></html>"
            ).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    server.counter_lock = threading.Lock()
    server.flaky_count = 0
    thread = threading.Thread(target=lambda: server.serve_forever(poll_interval=0.05), daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
