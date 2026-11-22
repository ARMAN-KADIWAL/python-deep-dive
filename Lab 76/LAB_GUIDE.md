# Lab 76: Thread Synchronization - Managing Shared Resources with Locks — Complete Guide

Observe lost updates, protect a shared counter, demonstrate a controlled deadlock, compare prevention strategies and transfer items through a bounded condition-variable buffer.

Read, modify aur write milkar ek critical section banate hain. Join sirf wait karta hai; lock shared data protect karta hai. Deadlock demo apne isolated child process mein atakta hai aur parent usi child ko time limit par clean karta hai. Timeout se operation abandon ho sakta hai, isliye completion counts alag dikhte hain.

Follow [README.md](README.md) for setup, commands, ports and validation. These are the complete final modules, not the intermediate/truncated snippets from the supplied handout.

## counter_with_lock.py

```python
import threading
import time


counter = 0


counter_lock = threading.Lock()

def increment_counter_safe(thread_name, iterations):
    """Function to safely increment the global counter using locks"""
    global counter

    print(f"{thread_name} starting...")

    for i in range(iterations):

        with counter_lock:

            current_value = counter


            time.sleep(0.0001)


            counter = current_value + 1


        if i % 10000 == 0:
            print(f"{thread_name}: Iteration {i}, Counter = {counter}")

    print(f"{thread_name} finished. Final counter value seen: {counter}")

def increment_counter_manual_lock(thread_name, iterations):
    """Alternative implementation using manual lock acquire/release"""
    global counter

    print(f"{thread_name} starting (manual lock)...")

    for i in range(iterations):

        counter_lock.acquire()

        try:

            current_value = counter
            time.sleep(0.0001)
            counter = current_value + 1
        finally:

            counter_lock.release()

        if i % 10000 == 0:
            print(f"{thread_name}: Iteration {i}, Counter = {counter}")

    print(f"{thread_name} finished. Final counter value seen: {counter}")

def main():
    global counter

    print("=== Counter With Lock Demo ===")


    print("\n--- Using 'with' statement for lock management ---")
    counter = 0

    iterations_per_thread = 50000
    threads = []
    thread_names = ["Thread-A", "Thread-B", "Thread-C"]

    start_time = time.time()


    for name in thread_names:
        thread = threading.Thread(
            target=increment_counter_safe,
            args=(name, iterations_per_thread)
        )
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()

    end_time = time.time()


    expected_value = len(thread_names) * iterations_per_thread
    print(f"\n=== Results (with lock) ===")
    print(f"Expected counter value: {expected_value}")
    print(f"Actual counter value: {counter}")
    print(f"Difference: {expected_value - counter}")
    print(f"Execution time: {end_time - start_time:.2f} seconds")

    if counter == expected_value:
        print("✅ Synchronization successful! Counter value is correct.")
    else:
        print("❌ Synchronization failed! Counter value is incorrect.")

if __name__ == "__main__":
    main()
```

## counter_without_lock.py

```python
import threading
import time


counter = 0

def increment_counter(thread_name, iterations):
    """Function to increment the global counter"""
    global counter

    print(f"{thread_name} starting...")

    for i in range(iterations):

        current_value = counter


        time.sleep(0.0001)


        counter = current_value + 1

        if i % 10000 == 0:
            print(f"{thread_name}: Iteration {i}, Counter = {counter}")

    print(f"{thread_name} finished. Final counter value seen: {counter}")

def main():
    global counter

    print("=== Counter Without Lock Demo ===")
    print("Starting with counter = 0")


    counter = 0


    iterations_per_thread = 50000


    threads = []
    thread_names = ["Thread-1", "Thread-2", "Thread-3"]


    start_time = time.time()


    for name in thread_names:
        thread = threading.Thread(
            target=increment_counter,
            args=(name, iterations_per_thread)
        )
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()


    end_time = time.time()


    expected_value = len(thread_names) * iterations_per_thread
    print(f"\n=== Results ===")
    print(f"Expected counter value: {expected_value}")
    print(f"Actual counter value: {counter}")
    print(f"Difference: {expected_value - counter}")
    print(f"Execution time: {end_time - start_time:.2f} seconds")

    if counter != expected_value:
        print("❌ Race condition detected! Counter value is incorrect.")
    else:
        print("✅ Counter value is correct (rare without synchronization).")

if __name__ == "__main__":
    main()
```

## deadlock_demo.py

```python
import multiprocessing as mp
import threading


def worker(first_lock, second_lock, barrier, name):
    with first_lock:
        print(f"{name}: first lock acquired", flush=True)
        barrier.wait()
        print(f"{name}: waiting for the other lock", flush=True)
        with second_lock:
            print(f"{name}: both locks acquired", flush=True)


def run_deadlock_scenario():
    lock1, lock2 = threading.Lock(), threading.Lock()
    barrier = threading.Barrier(2)
    threads = [
        threading.Thread(target=worker, args=(lock1, lock2, barrier, "Worker 1")),
        threading.Thread(target=worker, args=(lock2, lock1, barrier, "Worker 2")),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def demonstrate_deadlock(timeout=3):
    process = mp.get_context("spawn").Process(target=run_deadlock_scenario)
    process.start()
    try:
        process.join(timeout)
        if process.is_alive():
            print("DEADLOCK DETECTED: terminating only the isolated demonstration process.")
            return True
        raise RuntimeError("The intentional deadlock did not occur")
    finally:
        if process.is_alive():
            process.terminate()
        process.join()
        process.close()


def main():
    demonstrate_deadlock()
    print("PASS: Intentional deadlock detected and isolated process cleaned up.")


if __name__ == "__main__":
    mp.freeze_support()
    main()
```

## deadlock_prevention.py

```python
import queue
import threading
import time


def worker_ordered_locking(first_lock, second_lock):
    with first_lock:
        with second_lock:
            time.sleep(0.02)
            return True


def worker_timeout_approach(first_lock, second_lock):
    if not first_lock.acquire(timeout=0.2):
        return False
    try:
        time.sleep(0.01)
        if not second_lock.acquire(timeout=0.2):
            return False
        try:
            return True
        finally:
            second_lock.release()
    finally:
        first_lock.release()


def worker_try_lock_approach(first_lock, second_lock):
    for _ in range(20):
        if first_lock.acquire(blocking=False):
            try:
                if second_lock.acquire(blocking=False):
                    try:
                        return True
                    finally:
                        second_lock.release()
            finally:
                first_lock.release()
        time.sleep(0.01)
    return False


def run_strategy(strategy, reverse=False):
    lock1, lock2 = threading.Lock(), threading.Lock()
    outcomes = queue.Queue()

    def run(first, second):
        try:
            outcomes.put(strategy(first, second))
        except Exception as error:
            outcomes.put(error)

    second_pair = (lock2, lock1) if reverse else (lock1, lock2)
    threads = [threading.Thread(target=run, args=(lock1, lock2)), threading.Thread(target=run, args=second_pair)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=2)
    if any(thread.is_alive() for thread in threads):
        raise RuntimeError("Prevention strategy left a worker blocked")
    results = [outcomes.get_nowait() for _ in threads]
    for result in results:
        if isinstance(result, Exception):
            raise result
    print(f"{strategy.__name__}: {sum(results)}/2 operations completed; {results.count(False)} abandoned safely")
    if lock1.locked() or lock2.locked():
        raise RuntimeError("A prevention strategy leaked a lock")
    return results


def main():
    if run_strategy(worker_ordered_locking) != [True, True]:
        raise RuntimeError("Ordered locking failed to complete both operations")
    run_strategy(worker_timeout_approach, reverse=True)
    run_strategy(worker_try_lock_approach, reverse=True)
    print("PASS: All strategies returned without deadlock or leaked locks.")
    print("Timeout/retry approaches can abandon an operation; completion counts are shown above.")


if __name__ == "__main__":
    main()
```

## lock_comparison.py

```python
import threading
import time
import statistics


counter = 0
counter_lock = threading.Lock()

def increment_without_lock(iterations):
    """Increment counter without synchronization"""
    global counter
    for _ in range(iterations):
        current = counter
        time.sleep(0.00001)
        counter = current + 1

def increment_with_lock(iterations):
    """Increment counter with synchronization"""
    global counter
    for _ in range(iterations):
        with counter_lock:
            current = counter
            time.sleep(0.00001)
            counter = current + 1

def run_test(use_lock, num_threads, iterations_per_thread, test_name):
    """Run a single test scenario"""
    global counter
    counter = 0

    print(f"\n=== {test_name} ===")
    print(f"Threads: {num_threads}, Iterations per thread: {iterations_per_thread}")

    threads = []
    start_time = time.time()


    target_function = increment_with_lock if use_lock else increment_without_lock

    for i in range(num_threads):
        thread = threading.Thread(
            target=target_function,
            args=(iterations_per_thread,)
        )
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()

    end_time = time.time()


    expected = num_threads * iterations_per_thread
    actual = counter
    accuracy = (actual / expected) * 100 if expected > 0 else 0

    print(f"Expected: {expected}")
    print(f"Actual: {actual}")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Execution time: {end_time - start_time:.3f} seconds")

    return {
        'expected': expected,
        'actual': actual,
        'accuracy': accuracy,
        'time': end_time - start_time,
        'use_lock': use_lock
    }

def main():
    print("=== Thread Synchronization Comparison ===")

    test_scenarios = [
        (2, 1000),
        (3, 2000),
        (5, 1000),
    ]

    results = []

    for num_threads, iterations in test_scenarios:

        result_no_lock = run_test(
            False, num_threads, iterations,
            f"Without Lock - {num_threads} threads"
        )
        results.append(result_no_lock)


        result_with_lock = run_test(
            True, num_threads, iterations,
            f"With Lock - {num_threads} threads"
        )
        results.append(result_with_lock)


    print("\n" + "="*50)
    print("SUMMARY COMPARISON")
    print("="*50)

    no_lock_results = [r for r in results if not r['use_lock']]
    with_lock_results = [r for r in results if r['use_lock']]

    avg_accuracy_no_lock = statistics.mean([r['accuracy'] for r in no_lock_results])
    avg_accuracy_with_lock = statistics.mean([r['accuracy'] for r in with_lock_results])

    avg_time_no_lock = statistics.mean([r['time'] for r in no_lock_results])
    avg_time_with_lock = statistics.mean([r['time'] for r in with_lock_results])

    print(f"Average Accuracy Without Lock: {avg_accuracy_no_lock:.2f}%")
    print(f"Average Accuracy With Lock: {avg_accuracy_with_lock:.2f}%")
    print(f"Average Time Without Lock: {avg_time_no_lock:.3f} seconds")
    print(f"Average Time With Lock: {avg_time_with_lock:.3f} seconds")

    print(f"\nPerformance Impact: {((avg_time_with_lock - avg_time_no_lock) / avg_time_no_lock * 100):.1f}% slower with locks")
    print(f"Accuracy Improvement: {(avg_accuracy_with_lock - avg_accuracy_no_lock):.2f} percentage points higher with locks")

if __name__ == "__main__":
    main()
```

## producer_consumer.py

```python
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
```

