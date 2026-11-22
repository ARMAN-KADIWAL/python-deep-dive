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
from multi_server import MultiThreadedServer, SharedDataManager
from server_monitor import ServerMonitor


class MultiClientTests(unittest.TestCase):
    def test_history_and_stats_are_framed_together(self):
        with running_server(MultiThreadedServer("127.0.0.1", 0)) as server:
            client = MessageClient("127.0.0.1", server.port)
            try:
                client.connect()
                self.assertEqual(client.send_message("first"), "Echo from server: first")
                self.assertEqual(client.send_message("stats"), "Your message count: 2")
                history = client.send_message("history")
                self.assertIn("Recent messages:", history)
                self.assertIn("first", history)
                self.assertIn("Server time:", client.send_message("time"))
                self.assertEqual(client.send_message("quit"), "Goodbye!")
            finally:
                client.disconnect()
            wait_disconnected(server)
            self.assertEqual(server.shared_data.client_messages, {})

    def test_shared_data_is_thread_safe_and_bounded(self):
        manager = SharedDataManager()
        def worker(client_id):
            for i in range(50):
                manager.add_message(client_id, str(i))
        with ThreadPoolExecutor(max_workers=8) as executor:
            list(executor.map(worker, range(8)))
        self.assertEqual(len(manager.message_history), 100)
        self.assertEqual([manager.get_client_stats(i) for i in range(8)], [50] * 8)
        self.assertEqual(manager.get_recent_messages(0), [])
        copy = manager.get_recent_messages(1)
        copy[0]["message"] = "mutated"
        self.assertNotEqual(manager.get_recent_messages(1)[0]["message"], "mutated")

    def test_monitor_validates_all_responses(self):
        with running_server(MultiThreadedServer("127.0.0.1", 0)) as server:
            monitor = ServerMonitor("127.0.0.1", server.port)
            self.assertTrue(monitor.test_connection()[0])
            result = monitor.stress_test(5, 10)
            self.assertEqual(result["messages_verified"], 50)
            self.assertEqual(result["success"], 5)
            self.assertEqual(result["failed"], 0)
            wait_disconnected(server)

    def test_automated_client_and_multi_client_cli(self):
        with running_server(MultiThreadedServer("127.0.0.1", 0)) as server:
            output = run_client("test_client.py", server.port, ("--automated", "--messages", "7"))
            self.assertIn("received 7 responses", output)
            output = run_client("multi_client_test.py", server.port, ("--clients", "5"))
            self.assertIn("30 regular responses verified", output)
            output = run_client("server_monitor.py", server.port)
            self.assertIn("messages_verified", output)
            wait_disconnected(server)

    def test_shutdown_leaves_no_client_threads(self):
        with running_server(MultiThreadedServer("127.0.0.1", 0)) as server:
            clients = [MessageClient("127.0.0.1", server.port) for _ in range(3)]
            try:
                for client in clients:
                    client.connect()
                server.shutdown_server()
            finally:
                for client in clients:
                    client.disconnect()
            self.assertEqual(server.get_server_stats()["active_clients"], 0)
            self.assertFalse(any(thread.is_alive() for thread in server._threads))

    def test_idle_timeout_cleans_up_partial_frame(self):
        with running_server(MultiThreadedServer("127.0.0.1", 0, client_timeout=0.05)) as server:
            with socket.create_connection(("127.0.0.1", server.port), timeout=2) as client:
                self.assertIsNotNone(receive_message(client))
                client.sendall(b"\x00")
                self.assertIsNone(receive_message(client))
            wait_disconnected(server)


if __name__ == "__main__":
    unittest.main()
