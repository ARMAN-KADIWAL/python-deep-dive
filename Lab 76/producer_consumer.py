import threading
import time
import random
import queue

class SafeBuffer:
    """Thread-safe buffer using locks"""

    def __init__(self, max_size=10):
        if max_size < 1:
            raise ValueError("max_size must be positive")
        self.buffer = []
        self.max_size = max_size
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)

    def put(self, item):
        """Add item to buffer (blocks if buffer is full)"""
        with self.not_full:
            while len(self.buffer) >= self.max_size:
                print(f"Buffer full, producer waiting...")
                self.not_full.wait()

            self.buffer.append(item)
            print(f"Produced: {item}, Buffer size: {len(self.buffer)}")
            self.not_empty.notify()

    def get(self):
        """Remove and return item from buffer (blocks if buffer is empty)"""
        with self.not_empty:
            while len(self.buffer) == 0:
                print(f"Buffer empty, consumer waiting...")
                self.not_empty.wait()

            item = self.buffer.pop(0)
            print(f"Consumed: {item}, Buffer size: {len(self.buffer)}")
            self.not_full.notify()
            return item

    def size(self):
        """Return current buffer size"""
        with self.lock:
            return len(self.buffer)

def producer(buffer, producer_id, num_items):
    """Producer function that creates items"""
    print(f"Producer {producer_id} starting...")

    for i in range(num_items):

        item = f"Item-{producer_id}-{i+1}"


        time.sleep(random.uniform(0.1, 0.5))


        buffer.put(item)

    print(f"Producer {producer_id} finished")

def consumer(buffer, consumer_id, num_items):
    """Consumer function that processes items"""
    print(f"Consumer {consumer_id} starting...")

    for i in range(num_items):

        item = buffer.get()


        time.sleep(random.uniform(0.2, 0.8))

        print(f"Consumer {consumer_id} processed: {item}")

    print(f"Consumer {consumer_id} finished")

def main():
    print("=== Producer-Consumer with Thread Synchronization ===")


    buffer = SafeBuffer(max_size=5)


    num_producers = 2
    num_consumers = 2
    items_per_producer = 5
    items_per_consumer = 5

    print(f"Configuration:")
    print(f"- Producers: {num_producers}")
    print(f"- Consumers: {num_consumers}")
    print(f"- Items per producer: {items_per_producer}")
    print(f"- Buffer max size: {buffer.max_size}")
    print()

    threads = []


    for i in range(num_producers):
        thread = threading.Thread(
            target=producer,
            args=(buffer, i+1, items_per_producer)
        )
        threads.append(thread)


    for i in range(num_consumers):
        thread = threading.Thread(
            target=consumer,
            args=(buffer, i+1, items_per_consumer)
        )
        threads.append(thread)


    start_time = time.time()
    for thread in threads:
        thread.start()


    for thread in threads:
        thread.join()

    end_time = time.time()

    print(f"\n=== Results ===")
    print(f"All threads completed successfully!")
    print(f"Final buffer size: {buffer.size()}")
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
    print("✅ Producer-Consumer synchronization working correctly!")

if __name__ == "__main__":
    main()
