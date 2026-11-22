import argparse
import signal
import socket
import struct
import threading
import time
from datetime import datetime, timezone


MAX_MESSAGE_BYTES = 1024 * 1024


def receive_exact(sock, length, allow_eof=False):
    chunks = bytearray()
    while len(chunks) < length:
        chunk = sock.recv(length - len(chunks))
        if not chunk:
            if allow_eof and not chunks:
                return None
            raise EOFError("Connection ended in the middle of a message")
        chunks.extend(chunk)
    return bytes(chunks)


def send_message(sock, message):
    payload = message.encode("utf-8")
    if len(payload) > MAX_MESSAGE_BYTES:
        raise ValueError("Message exceeds the 1 MiB limit")
    sock.sendall(struct.pack("!I", len(payload)) + payload)


def receive_message(sock):
    header = receive_exact(sock, 4, allow_eof=True)
    if header is None:
        return None
    length = struct.unpack("!I", header)[0]
    if length > MAX_MESSAGE_BYTES:
        raise ValueError("Incoming message exceeds the 1 MiB limit")
    return receive_exact(sock, length).decode("utf-8")


def close_socket(sock):
    if sock is not None:
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        sock.close()


class FramedTCPServer:
    def __init__(self, host="localhost", port=8888, threaded=True, client_timeout=30):
        self.host = host
        self.port = port
        self.threaded = threaded
        self.client_timeout = client_timeout
        self.server_socket = None
        self.clients = {}
        self.client_lock = threading.RLock()
        self.running = False
        self.ready = threading.Event()
        self._stop = threading.Event()
        self._threads = set()
        self._connection_count = 0
        self.startup_error = None

    def greeting(self, client_id):
        return None

    def process_client_message(self, message, client_id):
        return f"Server received: {message}"

    def should_disconnect(self, message):
        return message.strip().lower() in {"quit", "exit", "bye"}

    def after_disconnect(self, client_id):
        pass

    def start_server(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
                self.server_socket = listener
                listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                listener.bind((self.host, self.port))
                self.port = listener.getsockname()[1]
                listener.listen(128)
                listener.settimeout(0.2)
                self.running = True
                self.ready.set()
                print(f"Server started on {self.host}:{self.port}", flush=True)
                while not self._stop.is_set():
                    try:
                        connection, address = listener.accept()
                    except socket.timeout:
                        continue
                    except OSError:
                        if self._stop.is_set():
                            break
                        raise
                    connection.settimeout(self.client_timeout)
                    connection.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                    with self.client_lock:
                        self._connection_count += 1
                        client_id = f"client-{self._connection_count}"
                        self.clients[connection] = {
                            "id": client_id,
                            "address": address,
                            "connected_at": datetime.now(timezone.utc).isoformat(),
                            "started": time.monotonic(),
                        }
                    if self.threaded:
                        thread = threading.Thread(target=self.handle_client, args=(connection, address))
                        with self.client_lock:
                            self._threads.add(thread)
                        thread.start()
                    else:
                        self.handle_client(connection, address)
        except KeyboardInterrupt:
            pass
        except Exception as error:
            self.startup_error = error
            raise
        finally:
            self.ready.set()
            self.shutdown_server()

    def handle_client(self, connection, address):
        with self.client_lock:
            client_id = self.clients[connection]["id"]
        try:
            welcome = self.greeting(client_id)
            if welcome is not None:
                send_message(connection, welcome)
            while not self._stop.is_set():
                message = receive_message(connection)
                if message is None:
                    break
                response = self.process_client_message(message, client_id)
                send_message(connection, response)
                if self.should_disconnect(message):
                    break
        except (OSError, EOFError, UnicodeError, ValueError):
            pass
        finally:
            close_socket(connection)
            self.after_disconnect(client_id)
            with self.client_lock:
                self.clients.pop(connection, None)
                self._threads.discard(threading.current_thread())

    def get_server_stats(self):
        with self.client_lock:
            details = [
                {"id": item["id"], "connected_at": item["connected_at"],
                 "duration_seconds": time.monotonic() - item["started"]}
                for item in self.clients.values()
            ]
            return {"active_clients": len(details), "total_connections": self._connection_count,
                    "client_details": details}

    def shutdown_server(self):
        self._stop.set()
        self.running = False
        with self.client_lock:
            connections = list(self.clients)
            threads = list(self._threads)
        for connection in connections:
            close_socket(connection)
        close_socket(self.server_socket)
        for thread in threads:
            if thread is not threading.current_thread():
                thread.join(timeout=2)

    cleanup = shutdown_server
    cleanup_server = shutdown_server


def run_server(server_type, default_port):
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=default_port)
    args = parser.parse_args()
    server = server_type(host=args.host, port=args.port)
    signal.signal(signal.SIGTERM, lambda *_: server.shutdown_server())
    try:
        server.start_server()
    finally:
        server.shutdown_server()
