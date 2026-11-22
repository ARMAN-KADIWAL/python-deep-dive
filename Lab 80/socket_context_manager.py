import socket
from contextlib import contextmanager
from network_core import receive_message, send_message


@contextmanager
def tcp_socket(host="localhost", port=8888):
    with socket.create_connection((host, port), timeout=5) as connection:
        yield connection


def test_context_manager(host="localhost", port=8888):
    message = "Hello from context manager!"
    with tcp_socket(host, port) as connection:
        send_message(connection, message)
        response = receive_message(connection)
        if response != f"Server received: {message}":
            raise RuntimeError("Incorrect server response")
        print(response)
    print("Socket closed automatically.")
    return response


if __name__ == "__main__":
    test_context_manager()
