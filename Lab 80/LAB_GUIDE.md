# Lab 80: Socket Programming Basics - Introduction to Sockets — Complete Guide

Create TCP and UDP sockets, run matching clients and servers, handle complete TCP messages, close connections cleanly and verify full echo responses while measuring latency.

Socket communication ka endpoint hai. TCP byte stream hai: ek send ka matlab ek recv mein poora message milna nahi. network_core.py four-byte length header aur complete reads use karta hai. UDP mein har datagram ki boundary hoti hai, lekin delivery/order guarantee nahi. Matching client aur server versions saath use karo.

Follow [README.md](README.md) for setup, commands, ports and validation. These are the complete final modules, not the intermediate/truncated snippets from the supplied handout.

## basic_socket.py

```python
"""
Basic Socket Creation Example
This script demonstrates how to create a socket object
"""

import socket
import sys

def create_basic_socket():
    """Create and display basic socket information"""
    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created successfully!")
        print(f"Socket family: {sock.family}")
        print(f"Socket type: {sock.type}")
        print(f"Socket protocol: {sock.proto}")


        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"Hostname: {hostname}")
        print(f"Local IP: {local_ip}")


        sock.close()
        print("Socket closed successfully!")

    except socket.error as e:
        print(f"Error creating socket: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_basic_socket()
```

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

## robust_client.py

```python
import argparse
from client_core import MessageClient


class RobustTCPClient(MessageClient):
    def __init__(self, host="localhost", port=7777, **kwargs):
        super().__init__(host, port, **kwargs)

    interactive_session = MessageClient.interactive_mode
    cleanup = MessageClient.disconnect


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=7777)
    args = parser.parse_args()
    client = RobustTCPClient(args.host, args.port)
    try:
        client.connect()
        client.interactive_session()
    finally:
        client.cleanup()
```

## robust_server.py

```python
from datetime import datetime, timezone
from network_core import FramedTCPServer, run_server


class RobustTCPServer(FramedTCPServer):
    def __init__(self, host="localhost", port=7777, **kwargs):
        super().__init__(host, port, **kwargs)

    def greeting(self, client_id):
        return "Welcome! Type help for available commands."

    def process_client_message(self, message, client_id):
        command = message.strip()
        lowered = command.lower()
        if lowered == "help":
            return "Available commands:\ntime: Server time\necho <message>: Echo text\nquit/exit/bye: Close connection"
        if lowered == "time":
            return f"Server time: {datetime.now(timezone.utc).isoformat()}"
        if lowered.startswith("echo "):
            return f"Echo: {command[5:]}"
        if self.should_disconnect(command):
            return "Goodbye!"
        return f"Unknown command: {command}\nType help for available commands."


if __name__ == "__main__":
    run_server(RobustTCPServer, 7777)
```

## socket_comparison.py

```python
"""
Socket Type Comparison
Demonstrates differences between TCP and UDP
"""

import socket
import time

def tcp_example():
    """Demonstrate TCP socket characteristics"""
    print("=== TCP (SOCK_STREAM) Example ===")


    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f"TCP Socket Type: {tcp_socket.type}")
    print("TCP Characteristics:")
    print("- Connection-oriented")
    print("- Reliable data delivery")
    print("- Ordered data transmission")
    print("- Error checking and correction")
    print("- Stream reliability adds protocol overhead; performance depends on workload")

    tcp_socket.close()
    print()

def udp_example():
    """Demonstrate UDP socket characteristics"""
    print("=== UDP (SOCK_DGRAM) Example ===")


    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print(f"UDP Socket Type: {udp_socket.type}")
    print("UDP Characteristics:")
    print("- Connectionless")
    print("- No delivery guarantee")
    print("- No order guarantee")
    print("- Minimal error checking")
    print("- Datagram overhead is lower; application performance depends on workload")

    udp_socket.close()
    print()

def socket_options_demo():
    """Demonstrate common socket options"""
    print("=== Socket Options Demo ===")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    reuse_addr = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    recv_buffer = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    send_buffer = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)

    print(f"SO_REUSEADDR: {reuse_addr}")
    print(f"Receive Buffer Size: {recv_buffer} bytes")
    print(f"Send Buffer Size: {send_buffer} bytes")


    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("SO_REUSEADDR enabled")

    sock.close()

if __name__ == "__main__":
    tcp_example()
    udp_example()
    socket_options_demo()
```

## socket_context_manager.py

```python
import socket
from contextlib import contextmanager
from network_core import receive_message, send_message


@contextmanager
def tcp_socket(host="localhost", port=8888):
    with socket.create_connection((host, port), timeout=5) as connection:
        yield connection


def test_context_manager(host="localhost", port=8888):
    message = "Hello from context manager!"
    with tcp_socket(host, port) as connection:
        send_message(connection, message)
        response = receive_message(connection)
        if response != f"Server received: {message}":
            raise RuntimeError("Incorrect server response")
        print(response)
    print("Socket closed automatically.")
    return response


if __name__ == "__main__":
    test_context_manager()
```

## socket_performance_test.py

```python
import argparse
import socket
import statistics
import time
from network_core import MAX_MESSAGE_BYTES, receive_message, send_message


class SocketPerformanceTester:
    def __init__(self, host="localhost", port=8888):
        self.host, self.port = host, port
        self.results = []

    def test_tcp_performance(self, num_messages=100, message_size=1024):
        if num_messages < 1 or not 1 <= message_size <= MAX_MESSAGE_BYTES - 100:
            raise ValueError("Use positive message counts and a payload smaller than 1 MiB - 100 bytes")
        self.results = []
        message = "A" * message_size
        expected = f"Server received: {message}"
        with socket.create_connection((self.host, self.port), timeout=5) as connection:
            started = time.perf_counter()
            for _ in range(num_messages):
                sent = time.perf_counter()
                send_message(connection, message)
                if receive_message(connection) != expected:
                    raise RuntimeError("Incomplete or incorrect echo response")
                self.results.append((time.perf_counter() - sent) * 1000)
            elapsed = time.perf_counter() - started
        return self.print_performance_stats(elapsed, num_messages, message_size)

    def print_performance_stats(self, total_time, num_messages, message_size):
        if total_time <= 0 or len(self.results) != num_messages:
            raise ValueError("Statistics require a positive duration and one sample per message")
        result = {
            "messages": num_messages, "payload_bytes": message_size,
            "elapsed_seconds": total_time,
            "mean_rtt_ms": statistics.mean(self.results),
            "median_rtt_ms": statistics.median(self.results),
            "min_rtt_ms": min(self.results), "max_rtt_ms": max(self.results),
            "messages_per_second": num_messages / total_time,
            "sent_payload_bytes_per_second": num_messages * message_size / total_time,
        }
        for name, value in result.items():
            print(f"{name}: {value:.4f}" if isinstance(value, float) else f"{name}: {value}")
        print("PASS: Every complete echo response verified.")
        print("Payload rate excludes response bytes, frame headers and network overhead.")
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8888)
    parser.add_argument("--messages", type=int, default=100)
    parser.add_argument("--size", type=int, default=1024)
    args = parser.parse_args()
    SocketPerformanceTester(args.host, args.port).test_tcp_performance(args.messages, args.size)
```

## tcp_client.py

```python
import argparse
from client_core import MessageClient


class TCPClient(MessageClient):
    def connect_to_server(self):
        return self.connect(expect_welcome=False)

    send_messages = MessageClient.interactive_mode
    cleanup = MessageClient.disconnect


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8888)
    args = parser.parse_args()
    client = TCPClient(args.host, args.port)
    try:
        client.connect_to_server()
        client.send_messages()
    finally:
        client.cleanup()
```

## tcp_server.py

```python
from network_core import FramedTCPServer, run_server


class TCPServer(FramedTCPServer):
    pass


if __name__ == "__main__":
    run_server(TCPServer, 8888)
```

## udp_client.py

```python
import argparse
import socket


class UDPClient:
    def __init__(self, host="localhost", port=9999):
        self.host, self.port = host, port

    def send_message(self, message):
        payload = message.encode("utf-8")
        if len(payload) > 65400:
            raise ValueError("UDP payload is too large")
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as connection:
            connection.settimeout(5)
            connection.sendto(payload, (self.host, self.port))
            response, _ = connection.recvfrom(65535)
            return response.decode("utf-8")

    def start_client(self):
        try:
            while True:
                message = input("UDP Client> ")
                if message.strip().lower() == "quit":
                    break
                print(self.send_message(message))
        except (EOFError, KeyboardInterrupt):
            print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=9999)
    args = parser.parse_args()
    UDPClient(args.host, args.port).start_client()
```

## udp_server.py

```python
import argparse
import socket
import threading


class UDPServer:
    def __init__(self, host="localhost", port=9999):
        self.host, self.port = host, port
        self.server_socket = None
        self.ready = threading.Event()
        self._stop = threading.Event()
        self.startup_error = None

    def start_server(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as connection:
                self.server_socket = connection
                connection.bind((self.host, self.port))
                self.port = connection.getsockname()[1]
                connection.settimeout(0.2)
                self.ready.set()
                print(f"UDP server started on {self.host}:{self.port}", flush=True)
                while not self._stop.is_set():
                    try:
                        payload, address = connection.recvfrom(65535)
                        message = payload.decode("utf-8")
                        response = f"UDP Server received: {message}".encode("utf-8")
                        if len(response) > 65507:
                            response = b"Error: response would exceed the UDP datagram limit"
                        connection.sendto(response, address)
                    except socket.timeout:
                        continue
                    except UnicodeDecodeError:
                        connection.sendto(b"Error: invalid UTF-8", address)
                    except OSError:
                        if self._stop.is_set():
                            break
                        raise
        except KeyboardInterrupt:
            pass
        except Exception as error:
            self.startup_error = error
            raise
        finally:
            self.ready.set()
            self.cleanup()

    def cleanup(self):
        self._stop.set()
        if self.server_socket is not None:
            self.server_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=9999)
    args = parser.parse_args()
    UDPServer(args.host, args.port).start_server()
```

