from network_core import run_server
from server_threaded import ThreadedServer


class SingleClientServer(ThreadedServer):
    def __init__(self, host="localhost", port=12345, **kwargs):
        super().__init__(host, port, threaded=False, **kwargs)


def main():
    run_server(SingleClientServer, 12345)


if __name__ == "__main__":
    main()
