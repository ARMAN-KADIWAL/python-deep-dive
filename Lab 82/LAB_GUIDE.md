# Lab 82: Multi-client Server with Threading — Complete Guide

Combine per-client threads, locked shared history/counters, complete messages, automated clients, verified stress tests and graceful shutdown.

Har client ka message count lock ke andar update hota hai. History last 100 messages tak bounded hai. Disconnect par active registry aur per-client counter clean hote hain. Server monitor har expected echo check karta hai; sirf response milne ko successful test nahi maanta.

Follow [README.md](README.md) for setup, commands, ports and validation. These are the complete final modules, not the intermediate/truncated snippets from the supplied handout.

## client_core.py

```python
import socket
from network_core import close_socket, receive_message, send_message


class MessageClient:
    def __init__(self, host="localhost", port=8888, timeout=5):
        self.host, self.port = host, port
        self.timeout = timeout
        self.socket = None
        self.welcome = None

    def connect(self, expect_welcome=True):
        self.socket = socket.create_connection((self.host, self.port), timeout=self.timeout)
        if expect_welcome:
            self.welcome = receive_message(self.socket)
            if self.welcome is None:
                self.disconnect()
                raise ConnectionError("Server closed before its welcome message")
        return True

    def send_message(self, message):
        if self.socket is None:
            raise ConnectionError("Client is not connected")
        send_message(self.socket, message)
        response = receive_message(self.socket)
        if response is None:
            raise ConnectionError("Server closed before responding")
        return response

    def disconnect(self):
        close_socket(self.socket)
        self.socket = None

    def interactive_mode(self):
        if self.welcome:
            print(self.welcome)
        try:
            while True:
                message = input("Client> ")
                if not message:
                    continue
                print(self.send_message(message))
                if message.strip().lower() in {"quit", "exit", "bye"}:
                    break
        except (EOFError, KeyboardInterrupt):
            print()
        finally:
            self.disconnect()
```

## multi_client_test.py

```python
import argparse
from concurrent.futures import ThreadPoolExecutor
from test_client import TestClient


def launch_client(client_id, host="localhost", port=8888):
    client = TestClient(host, port, f"Client-{client_id}")
    try:
        client.connect()
        responses = client.automated_test(6)
        if client.send_message("quit") != "Goodbye!":
            raise RuntimeError("Missing quit acknowledgement")
        return len(responses)
    finally:
        client.disconnect()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8888)
    parser.add_argument("--clients", type=int, default=5)
    args = parser.parse_args()
    if not 1 <= args.clients <= 20:
        parser.error("clients must be between 1 and 20")
    with ThreadPoolExecutor(max_workers=args.clients) as executor:
        results = list(executor.map(lambda i: launch_client(i, args.host, args.port), range(args.clients)))
    print(f"PASS: {len(results)} clients completed; {sum(results)} regular responses verified.")


if __name__ == "__main__":
    main()
```

## multi_server.py

```python
import threading
from collections import deque
from datetime import datetime, timezone
from network_core import FramedTCPServer, run_server


class SharedDataManager:
    def __init__(self):
        self.data_lock = threading.Lock()
        self.message_history = deque(maxlen=100)
        self.client_messages = {}

    def add_message(self, client_id, message):
        with self.data_lock:
            self.message_history.append({"client_id": client_id, "message": message,
                                         "timestamp": datetime.now(timezone.utc)})
            self.client_messages[client_id] = self.client_messages.get(client_id, 0) + 1

    def get_recent_messages(self, count=10):
        if count < 0:
            raise ValueError("count must be non-negative")
        with self.data_lock:
            entries = list(self.message_history)[-count:] if count else []
            return [dict(entry) for entry in entries]

    def get_client_stats(self, client_id):
        with self.data_lock:
            return self.client_messages.get(client_id, 0)

    def remove_client(self, client_id):
        with self.data_lock:
            self.client_messages.pop(client_id, None)


class MultiThreadedServer(FramedTCPServer):
    def __init__(self, host="localhost", port=8888, **kwargs):
        super().__init__(host, port, **kwargs)
        self.shared_data = SharedDataManager()

    def greeting(self, client_id):
        return f"Welcome to Multi-threaded Server! Your ID: {client_id}"

    def process_client_message(self, message, client_id):
        command = message.strip().lower()
        self.shared_data.add_message(client_id, message)
        if command == "time":
            return f"Server time: {datetime.now(timezone.utc).isoformat()}"
        if command == "clients":
            return f"Active clients: {self.get_server_stats()['active_clients']}"
        if command == "info":
            return f"Your ID: {client_id}, Server: {self.host}:{self.port}"
        if command == "stats":
            return f"Your message count: {self.shared_data.get_client_stats(client_id)}"
        if command == "history":
            entries = self.shared_data.get_recent_messages(5)
            return "Recent messages:\n" + "\n".join(f"{item['client_id']}: {item['message']}" for item in entries)
        if self.should_disconnect(command):
            return "Goodbye!"
        return f"Echo from server: {message}"

    def after_disconnect(self, client_id):
        self.shared_data.remove_client(client_id)


if __name__ == "__main__":
    run_server(MultiThreadedServer, 8888)
```

## network_core.py

```python
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
```

## server_monitor.py

```python
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from client_core import MessageClient


class ServerMonitor:
    def __init__(self, host="localhost", port=8888):
        self.host, self.port = host, port

    def test_connection(self):
        client = MessageClient(self.host, self.port)
        try:
            client.connect()
            response = client.send_message("time")
            if not response.startswith("Server time:"):
                raise RuntimeError("Unexpected time response")
            client.send_message("quit")
            return True, response
        except (OSError, EOFError, ValueError, RuntimeError) as error:
            return False, str(error)
        finally:
            client.disconnect()

    def stress_test(self, num_clients=5, messages_per_client=10):
        if not 1 <= num_clients <= 20 or not 1 <= messages_per_client <= 1000:
            raise ValueError("Use 1-20 clients and 1-1000 messages per client")

        def worker(client_id):
            client = MessageClient(self.host, self.port)
            try:
                client.connect()
                for i in range(messages_per_client):
                    message = f"StressTest-{client_id}-{i}"
                    if client.send_message(message) != f"Echo from server: {message}":
                        raise RuntimeError("Incorrect stress-test echo")
                if client.send_message("quit") != "Goodbye!":
                    raise RuntimeError("Missing quit acknowledgement")
                return messages_per_client
            finally:
                client.disconnect()

        started = time.perf_counter()
        result = {"success": 0, "failed": 0, "messages_verified": 0}
        with ThreadPoolExecutor(max_workers=num_clients) as executor:
            futures = [executor.submit(worker, i) for i in range(num_clients)]
            for future in as_completed(futures):
                try:
                    result["messages_verified"] += future.result()
                    result["success"] += 1
                except (OSError, EOFError, ValueError, RuntimeError):
                    result["failed"] += 1
        result["total_time"] = time.perf_counter() - started
        print(result)
        if result["failed"]:
            raise RuntimeError("One or more stress-test clients failed")
        return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8888)
    args = parser.parse_args()
    monitor = ServerMonitor(args.host, args.port)
    success, response = monitor.test_connection()
    if not success:
        raise RuntimeError(response)
    print(response)
    monitor.stress_test(3, 5)


if __name__ == "__main__":
    main()
```

## test_client.py

```python
import argparse
from client_core import MessageClient


class TestClient(MessageClient):
    def __init__(self, host="localhost", port=8888, client_name="Client", **kwargs):
        super().__init__(host, port, **kwargs)
        self.client_name = client_name

    def automated_test(self, num_messages=5):
        if num_messages < 1:
            raise ValueError("num_messages must be positive")
        messages = ["Hello from automated client", "time", "clients", "Test message", "stats"]
        responses = [self.send_message(messages[i % len(messages)]) for i in range(num_messages)]
        if any(not response for response in responses):
            raise RuntimeError("Server returned an empty response")
        print(f"PASS: {self.client_name} received {len(responses)} responses.")
        return responses


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", nargs="?", default="Client")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8888)
    parser.add_argument("--automated", action="store_true")
    parser.add_argument("--messages", type=int, default=5)
    args = parser.parse_args()
    client = TestClient(args.host, args.port, args.name)
    try:
        client.connect()
        if args.automated:
            client.automated_test(args.messages)
            print(client.send_message("quit"))
        else:
            client.interactive_mode()
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
```

