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
