from datetime import datetime, timezone
from network_core import FramedTCPServer, run_server


class ThreadedServer(FramedTCPServer):
    def __init__(self, host="localhost", port=12345, **kwargs):
        super().__init__(host, port, **kwargs)

    def greeting(self, client_id):
        return f"Welcome to the server, {client_id}! Type help for commands."

    def process_client_message(self, message, client_id):
        command = message.strip().lower()
        if self.should_disconnect(command):
            return "Goodbye! Connection closing."
        if command == "hello":
            return "Hello there! How can I help you?"
        if command == "time":
            return f"Current server time: {datetime.now(timezone.utc).isoformat()}"
        if command == "clients":
            return f"Currently connected clients: {self.get_server_stats()['active_clients']}"
        if command == "help":
            return "Available commands: hello, time, clients, help, exit"
        return f"Echo: {message}"


if __name__ == "__main__":
    run_server(ThreadedServer, 12345)
