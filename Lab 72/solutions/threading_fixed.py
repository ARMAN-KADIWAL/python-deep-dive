"""Synchronize the read-modify-write sequence with a lock."""

import threading


class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self, iterations=5):
        for _ in range(iterations):
            with self.lock:
                self.value += 1


def run_demo(workers=3, iterations=5):
    counter = Counter()
    threads = [
        threading.Thread(target=counter.increment, args=(iterations,))
        for _ in range(workers)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return counter.value


if __name__ == "__main__":
    print("Final counter:", run_demo())
    print("Expected counter:", 15)
