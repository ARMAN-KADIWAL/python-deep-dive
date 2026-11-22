import argparse
import socket
import statistics
import time
from network_core import MAX_MESSAGE_BYTES, receive_message, send_message


class SocketPerformanceTester:
    def __init__(self, host="localhost", port=8888):
        self.host, self.port = host, port
        self.results = []

    def test_tcp_performance(self, num_messages=100, message_size=1024):
        if num_messages < 1 or not 1 <= message_size <= MAX_MESSAGE_BYTES - 100:
            raise ValueError("Use positive message counts and a payload smaller than 1 MiB - 100 bytes")
        self.results = []
        message = "A" * message_size
        expected = f"Server received: {message}"
        with socket.create_connection((self.host, self.port), timeout=5) as connection:
            started = time.perf_counter()
            for _ in range(num_messages):
                sent = time.perf_counter()
                send_message(connection, message)
                if receive_message(connection) != expected:
                    raise RuntimeError("Incomplete or incorrect echo response")
                self.results.append((time.perf_counter() - sent) * 1000)
            elapsed = time.perf_counter() - started
        return self.print_performance_stats(elapsed, num_messages, message_size)

    def print_performance_stats(self, total_time, num_messages, message_size):
        if total_time <= 0 or len(self.results) != num_messages:
            raise ValueError("Statistics require a positive duration and one sample per message")
        result = {
            "messages": num_messages, "payload_bytes": message_size,
            "elapsed_seconds": total_time,
            "mean_rtt_ms": statistics.mean(self.results),
            "median_rtt_ms": statistics.median(self.results),
            "min_rtt_ms": min(self.results), "max_rtt_ms": max(self.results),
            "messages_per_second": num_messages / total_time,
            "sent_payload_bytes_per_second": num_messages * message_size / total_time,
        }
        for name, value in result.items():
            print(f"{name}: {value:.4f}" if isinstance(value, float) else f"{name}: {value}")
        print("PASS: Every complete echo response verified.")
        print("Payload rate excludes response bytes, frame headers and network overhead.")
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8888)
    parser.add_argument("--messages", type=int, default=100)
    parser.add_argument("--size", type=int, default=1024)
    args = parser.parse_args()
    SocketPerformanceTester(args.host, args.port).test_tcp_performance(args.messages, args.size)
