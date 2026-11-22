import contextlib
import socket
import struct
import subprocess
import sys
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from network_core import MAX_MESSAGE_BYTES, receive_message, send_message


@contextlib.contextmanager
def running_server(server):
    failures = []
    def run():
        try:
            server.start_server()
        except Exception as error:
            failures.append(error)
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    if not server.ready.wait(5) or server.startup_error:
        raise RuntimeError(f"Server failed to start: {server.startup_error}")
    try:
        yield server
    finally:
        cleanup = getattr(server, "shutdown_server", server.cleanup)
        cleanup()
        thread.join(timeout=5)
        if thread.is_alive():
            raise AssertionError("Server did not shut down")
        if failures:
            raise failures[0]


def wait_disconnected(server):
    deadline = time.monotonic() + 3
    while server.get_server_stats()["active_clients"] and time.monotonic() < deadline:
        time.sleep(0.01)
    if server.get_server_stats()["active_clients"]:
        raise AssertionError("Disconnected client leaked in the registry")


def run_client(script, port, extra=(), input_text=None):
    command = [sys.executable, str(Path(__file__).parent / script), "--host", "127.0.0.1", "--port", str(port), *extra]
    result = subprocess.run(command, input=input_text, capture_output=True, text=True, timeout=15)
    if result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)
    return result.stdout

class FramingTests(unittest.TestCase):
    def test_fragmented_utf8_message(self):
        first, second = socket.socketpair()
        payload = "Hello \u263a \u0627".encode("utf-8")
        frame = struct.pack("!I", len(payload)) + payload
        def write():
            with first:
                for byte in frame:
                    first.sendall(bytes([byte]))
        thread = threading.Thread(target=write)
        thread.start()
        with second:
            second.settimeout(2)
            self.assertEqual(receive_message(second), payload.decode("utf-8"))
            self.assertIsNone(receive_message(second))
        thread.join(timeout=2)

    def test_coalesced_frames_and_empty_message(self):
        first, second = socket.socketpair()
        with first, second:
            for message in ("one", "", "three"):
                send_message(first, message)
            self.assertEqual([receive_message(second) for _ in range(3)], ["one", "", "three"])

    def test_truncated_header_rejected(self):
        first, second = socket.socketpair()
        first.sendall(b"\x00\x00")
        first.close()
        with second:
            with self.assertRaises(EOFError):
                receive_message(second)

    def test_oversized_frame_rejected(self):
        first, second = socket.socketpair()
        with first, second:
            first.sendall(struct.pack("!I", MAX_MESSAGE_BYTES + 1))
            with self.assertRaises(ValueError):
                receive_message(second)

from robust_server import RobustTCPServer
from socket_context_manager import test_context_manager
from socket_performance_test import SocketPerformanceTester
from tcp_client import TCPClient
from tcp_server import TCPServer
from udp_client import UDPClient
from udp_server import UDPServer


class SocketTests(unittest.TestCase):
    def test_large_unicode_echo_and_quit(self):
        with running_server(TCPServer("127.0.0.1", 0)) as server:
            client = TCPClient("127.0.0.1", server.port)
            try:
                client.connect_to_server()
                message = "Hello \u263a" * 1000
                self.assertEqual(client.send_message(message), f"Server received: {message}")
                self.assertEqual(client.send_message("quit"), "Server received: quit")
            finally:
                client.cleanup()
            wait_disconnected(server)

    def test_performance_validates_full_echo_and_resets_samples(self):
        with running_server(TCPServer("127.0.0.1", 0)) as server:
            tester = SocketPerformanceTester("127.0.0.1", server.port)
            self.assertEqual(tester.test_tcp_performance(20, 8192)["messages"], 20)
            self.assertEqual(tester.test_tcp_performance(3, 32)["messages"], 3)
            self.assertEqual(len(tester.results), 3)
            output = run_client("socket_performance_test.py", server.port, ("--messages", "5", "--size", "256"))
            self.assertIn("Every complete echo response verified", output)

    def test_context_manager_closes_socket(self):
        with running_server(TCPServer("127.0.0.1", 0)) as server:
            response = test_context_manager("127.0.0.1", server.port)
            self.assertIn("Hello from context manager", response)
            wait_disconnected(server)

    def test_robust_interactive_commands(self):
        with running_server(RobustTCPServer("127.0.0.1", 0)) as server:
            output = run_client("robust_client.py", server.port, input_text="help\ntime\necho Hello World\nbye\n")
            self.assertIn("Available commands", output)
            self.assertIn("Server time:", output)
            self.assertIn("Echo: Hello World", output)
            self.assertIn("Goodbye!", output)

    def test_basic_interactive_client(self):
        with running_server(TCPServer("127.0.0.1", 0)) as server:
            output = run_client("tcp_client.py", server.port, input_text="hello\nquit\n")
            self.assertIn("Server received: hello", output)

    def test_udp_roundtrip(self):
        with running_server(UDPServer("127.0.0.1", 0)) as server:
            client = UDPClient("127.0.0.1", server.port)
            message = "Hello \u263a" * 500
            self.assertEqual(client.send_message(message), f"UDP Server received: {message}")
            output = run_client("udp_client.py", server.port, input_text="hello\nquit\n")
            self.assertIn("UDP Server received: hello", output)

    def test_invalid_tcp_encoding_does_not_kill_server(self):
        with running_server(TCPServer("127.0.0.1", 0)) as server:
            with socket.create_connection(("127.0.0.1", server.port), timeout=2) as client:
                client.sendall(struct.pack("!I", 1) + b"\xff")
                self.assertIsNone(receive_message(client))
            with socket.create_connection(("127.0.0.1", server.port), timeout=2) as client:
                send_message(client, "still alive")
                self.assertEqual(receive_message(client), "Server received: still alive")

    def test_shutdown_closes_idle_connection(self):
        with running_server(TCPServer("127.0.0.1", 0)) as server:
            with socket.create_connection(("127.0.0.1", server.port), timeout=2) as client:
                send_message(client, "ready")
                self.assertEqual(receive_message(client), "Server received: ready")
                server.shutdown_server()
                self.assertIsNone(receive_message(client))


if __name__ == "__main__":
    unittest.main()
