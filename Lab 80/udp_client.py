import argparse
import socket


class UDPClient:
    def __init__(self, host="localhost", port=9999):
        self.host, self.port = host, port

    def send_message(self, message):
        payload = message.encode("utf-8")
        if len(payload) > 65400:
            raise ValueError("UDP payload is too large")
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as connection:
            connection.settimeout(5)
            connection.sendto(payload, (self.host, self.port))
            response, _ = connection.recvfrom(65535)
            return response.decode("utf-8")

    def start_client(self):
        try:
            while True:
                message = input("UDP Client> ")
                if message.strip().lower() == "quit":
                    break
                print(self.send_message(message))
        except (EOFError, KeyboardInterrupt):
            print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=9999)
    args = parser.parse_args()
    UDPClient(args.host, args.port).start_client()
