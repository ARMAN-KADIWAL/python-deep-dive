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
