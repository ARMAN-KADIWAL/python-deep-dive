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

from client_core import MessageClient
from server import SingleClientServer
from server_threaded import ThreadedServer


class ClientServerTests(unittest.TestCase):
    def test_single_client_server_complete_commands(self):
        with running_server(SingleClientServer("127.0.0.1", 0)) as server:
            output = run_client("client.py", server.port, input_text="hello\ntime\nhelp\nexit\n")
            self.assertIn("Hello there!", output)
            self.assertIn("Current server time:", output)
            self.assertIn("Goodbye!", output)

    def test_many_clients_complete(self):
        with running_server(ThreadedServer("127.0.0.1", 0)) as server:
            output = run_client("test_multiple_clients.py", server.port, ("--clients", "8"))
            self.assertIn("All 8 clients completed", output)
            wait_disconnected(server)

    def test_clients_count_includes_all_connected_clients(self):
        with running_server(ThreadedServer("127.0.0.1", 0)) as server:
            clients = [MessageClient("127.0.0.1", server.port) for _ in range(3)]
            try:
                for client in clients:
                    client.connect()
                self.assertEqual(clients[0].send_message("clients"), "Currently connected clients: 3")
            finally:
                for client in clients:
                    client.disconnect()
            wait_disconnected(server)

    def test_large_message_is_not_truncated(self):
        with running_server(ThreadedServer("127.0.0.1", 0)) as server:
            client = MessageClient("127.0.0.1", server.port)
            try:
                client.connect()
                message = "x" * 20000
                self.assertEqual(client.send_message(message), f"Echo: {message}")
            finally:
                client.disconnect()


if __name__ == "__main__":
    unittest.main()
