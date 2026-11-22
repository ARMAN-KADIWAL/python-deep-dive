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
