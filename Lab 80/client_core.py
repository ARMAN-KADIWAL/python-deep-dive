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
