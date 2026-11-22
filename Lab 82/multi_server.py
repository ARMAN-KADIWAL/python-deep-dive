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
