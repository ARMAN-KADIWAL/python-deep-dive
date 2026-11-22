import argparse
from client_core import MessageClient


class TestClient(MessageClient):
    def __init__(self, host="localhost", port=8888, client_name="Client", **kwargs):
        super().__init__(host, port, **kwargs)
        self.client_name = client_name

    def automated_test(self, num_messages=5):
        if num_messages < 1:
            raise ValueError("num_messages must be positive")
        messages = ["Hello from automated client", "time", "clients", "Test message", "stats"]
        responses = [self.send_message(messages[i % len(messages)]) for i in range(num_messages)]
        if any(not response for response in responses):
            raise RuntimeError("Server returned an empty response")
        print(f"PASS: {self.client_name} received {len(responses)} responses.")
        return responses


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", nargs="?", default="Client")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8888)
    parser.add_argument("--automated", action="store_true")
    parser.add_argument("--messages", type=int, default=5)
    args = parser.parse_args()
    client = TestClient(args.host, args.port, args.name)
    try:
        client.connect()
        if args.automated:
            client.automated_test(args.messages)
            print(client.send_message("quit"))
        else:
            client.interactive_mode()
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
