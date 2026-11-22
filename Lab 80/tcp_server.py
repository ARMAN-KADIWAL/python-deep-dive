from network_core import FramedTCPServer, run_server


class TCPServer(FramedTCPServer):
    pass


if __name__ == "__main__":
    run_server(TCPServer, 8888)
