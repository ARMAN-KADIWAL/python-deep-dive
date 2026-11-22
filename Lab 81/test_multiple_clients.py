import argparse
from concurrent.futures import ThreadPoolExecutor
from client_core import MessageClient


def create_test_client(client_id, host="localhost", port=12345):
    client = MessageClient(host, port)
    try:
        client.connect()
        for message in ("hello", "time", "clients", f"Message from client {client_id}"):
            response = client.send_message(message)
            if not response or (message.startswith("Message") and message not in response):
                raise RuntimeError("Incorrect response")
        if "Goodbye" not in client.send_message("exit"):
            raise RuntimeError("Missing exit acknowledgement")
        return client_id
    finally:
        client.disconnect()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=12345)
    parser.add_argument("--clients", type=int, default=3)
    args = parser.parse_args()
    if not 1 <= args.clients <= 20:
        parser.error("clients must be between 1 and 20")
    with ThreadPoolExecutor(max_workers=args.clients) as pool:
        results = list(pool.map(lambda i: create_test_client(i, args.host, args.port), range(args.clients)))
    print(f"PASS: All {len(results)} clients completed their exchanges.")


if __name__ == "__main__":
    main()
