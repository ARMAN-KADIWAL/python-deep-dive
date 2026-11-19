import threading
import time
import random

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
    
    def increment(self, thread_name):
        for i in range(5):
            # Bug: Race condition without proper locking
            current = self.value
            time.sleep(random.uniform(0.01, 0.1))  # Simulate processing
            self.value = current + 1
            print(f"{thread_name}: incremented to {self.value}")

def worker_thread(counter, thread_name):
    print(f"Starting {thread_name}")
    counter.increment(thread_name)
    print(f"Finished {thread_name}")

def main():
    counter = Counter()
    threads = []
    
    # Create multiple threads
    for i in range(3):
        thread_name = f"Thread-{i+1}"
        thread = threading.Thread(target=worker_thread, args=(counter, thread_name))
        threads.append(thread)
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print(f"Final counter value: {counter.value}")
    print("Expected value: 15")

if __name__ == "__main__":
    main()
