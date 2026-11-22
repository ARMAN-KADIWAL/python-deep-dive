import argparse
from client_core import MessageClient


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=12345)
    args = parser.parse_args()
    client = MessageClient(args.host, args.port)
    try:
        client.connect()
        client.interactive_mode()
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
