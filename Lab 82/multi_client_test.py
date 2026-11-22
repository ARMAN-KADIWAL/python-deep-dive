import argparse
from concurrent.futures import ThreadPoolExecutor
from test_client import TestClient


def launch_client(client_id, host="localhost", port=8888):
    client = TestClient(host, port, f"Client-{client_id}")
    try:
        client.connect()
        responses = client.automated_test(6)
        if client.send_message("quit") != "Goodbye!":
            raise RuntimeError("Missing quit acknowledgement")
        return len(responses)
    finally:
        client.disconnect()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8888)
    parser.add_argument("--clients", type=int, default=5)
    args = parser.parse_args()
    if not 1 <= args.clients <= 20:
        parser.error("clients must be between 1 and 20")
    with ThreadPoolExecutor(max_workers=args.clients) as executor:
        results = list(executor.map(lambda i: launch_client(i, args.host, args.port), range(args.clients)))
    print(f"PASS: {len(results)} clients completed; {sum(results)} regular responses verified.")


if __name__ == "__main__":
    main()
