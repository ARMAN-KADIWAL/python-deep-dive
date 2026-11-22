import argparse
import socket
import threading


class UDPServer:
    def __init__(self, host="localhost", port=9999):
        self.host, self.port = host, port
        self.server_socket = None
        self.ready = threading.Event()
        self._stop = threading.Event()
        self.startup_error = None

    def start_server(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as connection:
                self.server_socket = connection
                connection.bind((self.host, self.port))
                self.port = connection.getsockname()[1]
                connection.settimeout(0.2)
                self.ready.set()
                print(f"UDP server started on {self.host}:{self.port}", flush=True)
                while not self._stop.is_set():
                    try:
                        payload, address = connection.recvfrom(65535)
                        message = payload.decode("utf-8")
                        response = f"UDP Server received: {message}".encode("utf-8")
                        if len(response) > 65507:
                            response = b"Error: response would exceed the UDP datagram limit"
                        connection.sendto(response, address)
                    except socket.timeout:
                        continue
                    except UnicodeDecodeError:
                        connection.sendto(b"Error: invalid UTF-8", address)
                    except OSError:
                        if self._stop.is_set():
                            break
                        raise
        except KeyboardInterrupt:
            pass
        except Exception as error:
            self.startup_error = error
            raise
        finally:
            self.ready.set()
            self.cleanup()

    def cleanup(self):
        self._stop.set()
        if self.server_socket is not None:
            self.server_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=9999)
    args = parser.parse_args()
    UDPServer(args.host, args.port).start_server()
