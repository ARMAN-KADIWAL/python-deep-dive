import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from client_core import MessageClient


class ServerMonitor:
    def __init__(self, host="localhost", port=8888):
        self.host, self.port = host, port

    def test_connection(self):
        client = MessageClient(self.host, self.port)
        try:
            client.connect()
            response = client.send_message("time")
            if not response.startswith("Server time:"):
                raise RuntimeError("Unexpected time response")
            client.send_message("quit")
            return True, response
        except (OSError, EOFError, ValueError, RuntimeError) as error:
            return False, str(error)
        finally:
            client.disconnect()

    def stress_test(self, num_clients=5, messages_per_client=10):
        if not 1 <= num_clients <= 20 or not 1 <= messages_per_client <= 1000:
            raise ValueError("Use 1-20 clients and 1-1000 messages per client")

        def worker(client_id):
            client = MessageClient(self.host, self.port)
            try:
                client.connect()
                for i in range(messages_per_client):
                    message = f"StressTest-{client_id}-{i}"
                    if client.send_message(message) != f"Echo from server: {message}":
                        raise RuntimeError("Incorrect stress-test echo")
                if client.send_message("quit") != "Goodbye!":
                    raise RuntimeError("Missing quit acknowledgement")
                return messages_per_client
            finally:
                client.disconnect()

        started = time.perf_counter()
        result = {"success": 0, "failed": 0, "messages_verified": 0}
        with ThreadPoolExecutor(max_workers=num_clients) as executor:
            futures = [executor.submit(worker, i) for i in range(num_clients)]
            for future in as_completed(futures):
                try:
                    result["messages_verified"] += future.result()
                    result["success"] += 1
                except (OSError, EOFError, ValueError, RuntimeError):
                    result["failed"] += 1
        result["total_time"] = time.perf_counter() - started
        print(result)
        if result["failed"]:
            raise RuntimeError("One or more stress-test clients failed")
        return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8888)
    args = parser.parse_args()
    monitor = ServerMonitor(args.host, args.port)
    success, response = monitor.test_connection()
    if not success:
        raise RuntimeError(response)
    print(response)
    monitor.stress_test(3, 5)


if __name__ == "__main__":
    main()
