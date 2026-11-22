# Lab 75: Introduction to Threading - Basic Threading in Python — Complete Guide

Create and join threads, compare equal CPU workloads, coordinate shared data with locks, run a real shared work queue, and inspect thread lifecycles.

Thread ek process ka worker hai. I/O wait ke dauraan doosra thread aage badh sakta hai. Shared counter ya bank balance update karte waqt same lock use karo. Worker pool mein sab workers ek common queue se jobs lete hain; har worker ko jobs ki alag copy nahi milti.

Follow [README.md](README.md) for setup, commands, ports and validation. These are the complete final modules, not the intermediate/truncated snippets from the supplied handout.

## advanced_locks.py

```python
import threading
import time
import random

class ResourcePool:
    """Thread-safe resource pool using RLock"""

    def __init__(self, max_resources=3):
        if max_resources < 1:
            raise ValueError("max_resources must be positive")
        self.max_resources = max_resources
        self.available_resources = list(range(1, max_resources + 1))
        self.in_use_resources = []
        self.lock = threading.RLock()

    def acquire_resource(self, client_name):
        """Acquire a resource from the pool"""
        with self.lock:
            if self.available_resources:
                resource = self.available_resources.pop(0)
                self.in_use_resources.append(resource)
                print(f"{client_name} acquired resource {resource}")
                return resource
            else:
                print(f"{client_name} waiting for resource...")
                return None

    def release_resource(self, resource, client_name):
        """Release a resource back to the pool"""
        with self.lock:
            if resource in self.in_use_resources:
                self.in_use_resources.remove(resource)
                self.available_resources.append(resource)
                print(f"{client_name} released resource {resource}")
                return True
            return False

    def get_status(self):
        """Get current pool status (demonstrates reentrant lock)"""
        with self.lock:
            return self._get_detailed_status()

    def _get_detailed_status(self):
        """Internal method that also needs the lock"""
        with self.lock:
            return {
                'available': len(self.available_resources),
                'in_use': len(self.in_use_resources),
                'available_resources': self.available_resources.copy(),
                'in_use_resources': self.in_use_resources.copy()
            }

def client_worker(client_name, resource_pool, work_duration):
    """Simulate a client using resources from the pool"""
    for i in range(3):
        print(f"{client_name} attempting to acquire resource (attempt {i+1})")


        resource = None
        while resource is None:
            resource = resource_pool.acquire_resource(client_name)
            if resource is None:
                time.sleep(0.5)


        print(f"{client_name} using resource {resource} for {work_duration} seconds")
        time.sleep(work_duration)


        resource_pool.release_resource(resource, client_name)


        time.sleep(0.2)

def demonstrate_resource_pool():
    """Demonstrate resource pool with multiple clients"""
    print("=== Resource Pool Demonstration ===")

    pool = ResourcePool(max_resources=2)


    clients = [
        ("Client-A", 2),
        ("Client-B", 1.5),
        ("Client-C", 1),
        ("Client-D", 2.5)
    ]

    threads = []

    for client_name, work_duration in clients:
        thread = threading.Thread(
            target=client_worker,
            args=(client_name, pool, work_duration)
        )
        threads.append(thread)
        thread.start()


    monitor_thread = threading.Thread(target=monitor_pool, args=(pool, 10))
    monitor_thread.daemon = True
    monitor_thread.start()


    for thread in threads:
        thread.join()

    print("All clients completed their work")
    final_status = pool.get_status()
    print(f"Final pool status: {final_status}")

def monitor_pool(pool, duration):
    """Monitor and display pool status periodically"""
    start_time = time.time()

    while time.time() - start_time < duration:
        status = pool.get_status()
        print(f"Pool Status - Available: {status['available']}, In Use: {status['in_use']}")
        time.sleep(1)

def deadlock_example():
    """Demonstrate potential deadlock scenario and how to avoid it"""
    print("\n=== Deadlock Prevention Example ===")

    lock1 = threading.Lock()
    lock2 = threading.Lock()

    def worker1():
        print("Worker 1: Acquiring lock1...")
        with lock1:
            print("Worker 1: Got lock1, working...")
            time.sleep(1)

            print("Worker 1: Acquiring lock2...")
            with lock2:
                print("Worker 1: Got both locks, doing work...")
                time.sleep(1)
        print("Worker 1: Released all locks")

    def worker2():
        print("Worker 2: Acquiring lock1...")
        with lock1:
            print("Worker 2: Got lock1, working...")
            time.sleep(1)

            print("Worker 2: Acquiring lock2...")
            with lock2:
                print("Worker 2: Got both locks, doing work...")
                time.sleep(1)
        print("Worker 2: Released all locks")


    thread1 = threading.Thread(target=worker1)
    thread2 = threading.Thread(target=worker2)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("Both workers completed successfully (no deadlock)")

def main():
    demonstrate_resource_pool()
    deadlock_example()

if __name__ == "__main__":
    main()
```

## advanced_threading.py

```python
import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor


class WorkerThread(threading.Thread):
    def __init__(self, thread_id, task_queue, completed, result_lock):
        super().__init__(name=f"Worker-{thread_id}")
        self.thread_id = thread_id
        self.task_queue = task_queue
        self.completed = completed
        self.result_lock = result_lock

    def run(self):
        while True:
            task = self.task_queue.get()
            try:
                if task is None:
                    return
                self.process_task(task)
                with self.result_lock:
                    self.completed.append(task)
            finally:
                self.task_queue.task_done()

    def process_task(self, task):
        time.sleep(0.1)
        print(f"{self.name} completed {task}")


def download_simulation(file_name, size_mb):
    for progress in range(0, 101, 20):
        time.sleep(0.1)
        print(f"{file_name} ({size_mb} MB): {progress}%")
    return file_name


def concurrent_downloads():
    files = [("document.pdf", 5), ("video.mp4", 50), ("music.mp3", 10), ("software.zip", 100)]
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda item: download_simulation(*item), files))
    return results


def worker_pool_example():
    tasks = [f"Task-{i}" for i in range(1, 11)]
    task_queue = queue.Queue()
    completed = []
    result_lock = threading.Lock()
    workers = [WorkerThread(i, task_queue, completed, result_lock) for i in range(1, 4)]
    for task in tasks:
        task_queue.put(task)
    for _ in workers:
        task_queue.put(None)
    for worker in workers:
        worker.start()
    task_queue.join()
    for worker in workers:
        worker.join()
    if sorted(completed) != sorted(tasks):
        raise RuntimeError("Worker pool lost or duplicated a task")
    print(f"PASS: {len(completed)} unique tasks processed exactly once.")
    return completed


def main():
    concurrent_downloads()
    worker_pool_example()


if __name__ == "__main__":
    main()
```

## basic_threading.py

```python
import threading
import time

def worker_function(thread_name, duration):
    """
    A simple worker function that simulates work by sleeping
    """
    print(f"Thread {thread_name} starting work...")
    time.sleep(duration)
    print(f"Thread {thread_name} finished work after {duration} seconds")

def main():
    print("=== Basic Threading Example ===")
    print("Main thread starting...")


    thread1 = threading.Thread(target=worker_function, args=("Worker-1", 2))
    thread2 = threading.Thread(target=worker_function, args=("Worker-2", 3))
    thread3 = threading.Thread(target=worker_function, args=("Worker-3", 1))


    print("Starting all threads...")
    start_time = time.time()

    thread1.start()
    thread2.start()
    thread3.start()


    thread1.join()
    thread2.join()
    thread3.join()

    end_time = time.time()
    total_time = end_time - start_time

    print(f"All threads completed in {total_time:.2f} seconds")
    print("Main thread ending...")

if __name__ == "__main__":
    main()
```

## gil_demonstration.py

```python
import threading
import time
import multiprocessing

def cpu_bound_task(n, thread_name):
    """
    CPU-intensive task that calculates sum of squares
    """
    print(f"{thread_name} starting CPU-bound task...")
    start_time = time.time()

    total = 0
    for i in range(n):
        total += i * i

    end_time = time.time()
    duration = end_time - start_time
    print(f"{thread_name} completed in {duration:.2f} seconds. Result: {total}")
    return total

def run_single_thread():
    """Run CPU-bound task in single thread"""
    print("\n=== Single Thread Execution ===")
    start_time = time.time()

    cpu_bound_task(10000000, "Single-Thread")
    cpu_bound_task(10000000, "Single-Thread")

    end_time = time.time()
    print(f"Total single-thread time: {end_time - start_time:.2f} seconds")

def run_multiple_threads():
    """Run CPU-bound tasks in multiple threads"""
    print("\n=== Multiple Threads Execution ===")
    start_time = time.time()


    thread1 = threading.Thread(target=cpu_bound_task, args=(10000000, "Thread-1"))
    thread2 = threading.Thread(target=cpu_bound_task, args=(10000000, "Thread-2"))


    thread1.start()
    thread2.start()


    thread1.join()
    thread2.join()

    end_time = time.time()
    print(f"Total multi-thread time: {end_time - start_time:.2f} seconds")

def io_bound_task(duration, thread_name):
    """IO-bound task simulation"""
    print(f"{thread_name} starting IO-bound task...")
    time.sleep(duration)
    print(f"{thread_name} completed IO-bound task")

def run_io_bound_threads():
    """Demonstrate threading effectiveness with IO-bound tasks"""
    print("\n=== IO-bound Tasks with Threading ===")
    start_time = time.time()

    threads = []
    for i in range(3):
        thread = threading.Thread(target=io_bound_task, args=(2, f"IO-Thread-{i+1}"))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"IO-bound threading time: {end_time - start_time:.2f} seconds")

def main():
    print("=== GIL Demonstration ===")
    print("This demonstrates how GIL affects CPU-bound vs IO-bound tasks")

    run_single_thread()
    run_multiple_threads()
    run_io_bound_threads()

    print("\nKey Observations:")
    print("1. CPU-bound tasks don't benefit much from threading due to GIL")
    print("2. IO-bound tasks benefit significantly from threading")
    print("3. For CPU-bound tasks, consider multiprocessing instead")

if __name__ == "__main__":
    main()
```

## performance_measurement.py

```python
import threading
import time
import statistics

def fibonacci(n):
    """Calculate fibonacci number (CPU-intensive)"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def measure_execution_time(func, *args):
    """Measure execution time of a function"""
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return end_time - start_time, result

def cpu_task(n, results, index):
    """CPU-bound task for threading"""
    result = fibonacci(n)
    results[index] = result

def compare_performance():
    """Compare single-thread vs multi-thread performance"""
    n = 30
    num_tasks = 2

    print("=== Performance Comparison ===")
    print(f"Calculating fibonacci({n}) {num_tasks} times")


    print("\nSingle-threaded execution:")
    start_time = time.time()
    single_results = []

    for i in range(num_tasks):
        result = fibonacci(n)
        single_results.append(result)
        print(f"Task {i+1} completed: {result}")

    single_time = time.time() - start_time
    print(f"Single-thread total time: {single_time:.2f} seconds")


    print("\nMulti-threaded execution:")
    start_time = time.time()
    threads = []
    thread_results = [None] * num_tasks

    for i in range(num_tasks):
        thread = threading.Thread(target=cpu_task, args=(n, thread_results, i))
        threads.append(thread)
        thread.start()

    for i, thread in enumerate(threads):
        thread.join()
        print(f"Thread {i+1} completed: {thread_results[i]}")

    multi_time = time.time() - start_time
    if thread_results != single_results:
        raise RuntimeError("Thread results differ from sequential results")
    print(f"Multi-thread total time: {multi_time:.2f} seconds")


    print(f"\nPerformance Analysis:")
    print(f"Single-thread time: {single_time:.2f}s")
    print(f"Multi-thread time: {multi_time:.2f}s")
    print(f"Speedup ratio: {single_time/multi_time:.2f}x")

    if multi_time >= single_time:
        print("Threading provided no speedup for CPU-bound tasks (due to GIL)")
    else:
        print("Threading provided speedup")

if __name__ == "__main__":
    compare_performance()
```

## race_condition_demo.py

```python
import threading
import time


shared_counter = 0

def unsafe_increment(thread_name, iterations):
    """Unsafe increment without synchronization"""
    global shared_counter

    for i in range(iterations):

        current_value = shared_counter
        time.sleep(0.0001)
        shared_counter = current_value + 1

        if i % 1000 == 0:
            print(f"{thread_name}: iteration {i}, counter = {shared_counter}")

def demonstrate_race_condition():
    """Demonstrate race condition problem"""
    global shared_counter
    shared_counter = 0

    print("=== Race Condition Demonstration ===")
    print("Running unsafe increment with multiple threads...")

    iterations = 5000
    num_threads = 3

    threads = []
    start_time = time.time()


    for i in range(num_threads):
        thread = threading.Thread(
            target=unsafe_increment,
            args=(f"Thread-{i+1}", iterations)
        )
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()

    end_time = time.time()
    expected_value = iterations * num_threads

    print(f"\nResults:")
    print(f"Expected counter value: {expected_value}")
    print(f"Actual counter value: {shared_counter}")
    print(f"Difference: {expected_value - shared_counter}")
    print(f"Execution time: {end_time - start_time:.2f} seconds")

    if shared_counter != expected_value:
        print("❌ Race condition detected! Counter value is incorrect.")
    else:
        print("✅ No race condition detected (lucky run).")

if __name__ == "__main__":
    demonstrate_race_condition()
```

## sequential_vs_concurrent.py

```python
import threading
import time

def task_function(task_id, duration):
    """Simulate a task that takes some time to complete"""
    print(f"Task {task_id} starting...")
    time.sleep(duration)
    print(f"Task {task_id} completed")

def run_sequential():
    """Run tasks one after another"""
    print("\n=== Sequential Execution ===")
    start_time = time.time()

    task_function(1, 2)
    task_function(2, 2)
    task_function(3, 2)

    end_time = time.time()
    print(f"Sequential execution time: {end_time - start_time:.2f} seconds")

def run_concurrent():
    """Run tasks concurrently using threads"""
    print("\n=== Concurrent Execution ===")
    start_time = time.time()


    threads = []
    for i in range(1, 4):
        thread = threading.Thread(target=task_function, args=(i, 2))
        threads.append(thread)


    for thread in threads:
        thread.start()


    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Concurrent execution time: {end_time - start_time:.2f} seconds")

def main():
    run_sequential()
    run_concurrent()

if __name__ == "__main__":
    main()
```

## thread_lifecycle.py

```python
import threading
import time

def long_running_task(task_name, duration):
    """A task that runs for a specified duration"""
    print(f"{task_name} started")

    for i in range(duration):
        print(f"{task_name} working... step {i+1}/{duration}")
        time.sleep(1)

    print(f"{task_name} completed")

def demonstrate_thread_states():
    """Demonstrate different thread states"""
    print("=== Thread Lifecycle Demonstration ===")


    thread = threading.Thread(target=long_running_task, args=("Background-Task", 5))

    print(f"Thread created. Is alive? {thread.is_alive()}")


    thread.start()
    print(f"Thread started. Is alive? {thread.is_alive()}")


    time.sleep(2)
    print(f"Thread running. Is alive? {thread.is_alive()}")


    thread.join()
    print(f"Thread joined. Is alive? {thread.is_alive()}")

def timeout_example():
    """Demonstrate thread join with timeout"""
    print("\n=== Thread Timeout Example ===")

    thread = threading.Thread(target=long_running_task, args=("Timeout-Task", 10))
    thread.start()


    print("Waiting for thread to complete (timeout: 3 seconds)...")
    thread.join(timeout=3)

    if thread.is_alive():
        print("Thread is still running after timeout")
        print("Continuing with other work...")


        time.sleep(2)
        print("Other work completed")


        print("Now waiting for thread to fully complete...")
        thread.join()
        print("Thread finally completed")
    else:
        print("Thread completed within timeout")

def main():
    demonstrate_thread_states()
    timeout_example()

if __name__ == "__main__":
    main()
```

## thread_monitoring.py

```python
import threading
import time
import os

def display_thread_info():
    """Display detailed information about the current thread"""
    current_thread = threading.current_thread()

    print(f"Thread Name: {current_thread.name}")
    print(f"Thread ID: {current_thread.ident}")
    print(f"Is Daemon: {current_thread.daemon}")
    print(f"Is Alive: {current_thread.is_alive()}")
    print(f"Process ID: {os.getpid()}")
    print("-" * 40)

def worker_with_info(task_name, duration):
    """Worker function that displays thread information"""
    print(f"\n=== {task_name} Starting ===")
    display_thread_info()

    print(f"{task_name} working for {duration} seconds...")
    for i in range(duration):
        time.sleep(1)
        current_thread = threading.current_thread()
        print(f"{task_name} ({current_thread.name}): Step {i+1}/{duration}")

    print(f"{task_name} completed!")
    display_thread_info()

def demonstrate_thread_info():
    """Demonstrate thread information gathering"""
    print("=== Thread Information Demonstration ===")


    print("Main Thread Information:")
    display_thread_info()


    threads = []

    for index, duration in enumerate((1, 2, 3), start=1):
        thread = threading.Thread(
            target=worker_with_info,
            args=(f"Task-{index}", duration),
            name=f"Monitor-Worker-{index}",
        )
        threads.append(thread)
        thread.start()

    print(f"Active thread count: {threading.active_count()}")
    for thread in threading.enumerate():
        print(f"Active: {thread.name}, id={thread.ident}, daemon={thread.daemon}")

    for thread in threads:
        thread.join()

    if any(thread.is_alive() for thread in threads):
        raise RuntimeError("A monitored worker did not finish")
    print("PASS: All monitored worker threads finished.")


if __name__ == "__main__":
    demonstrate_thread_info()
```

## thread_synchronization.py

```python
import threading
import time
import random


shared_counter = 0
counter_lock = threading.Lock()


class BankAccount:
    def __init__(self, initial_balance=1000):
        self.balance = initial_balance
        self.lock = threading.Lock()
        self.transaction_history = []

    def deposit(self, amount, account_holder):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        """Thread-safe deposit operation"""
        with self.lock:
            old_balance = self.balance
            time.sleep(0.1)
            self.balance += amount
            transaction = f"{account_holder} deposited ${amount}. Balance: ${old_balance} -> ${self.balance}"
            self.transaction_history.append(transaction)
            print(transaction)

    def withdraw(self, amount, account_holder):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        """Thread-safe withdrawal operation"""
        with self.lock:
            if self.balance >= amount:
                old_balance = self.balance
                time.sleep(0.1)
                self.balance -= amount
                transaction = f"{account_holder} withdrew ${amount}. Balance: ${old_balance} -> ${self.balance}"
                self.transaction_history.append(transaction)
                print(transaction)
                return True
            else:
                print(f"{account_holder} attempted to withdraw ${amount} but insufficient funds (${self.balance})")
                return False

    def get_balance(self):
        """Thread-safe balance check"""
        with self.lock:
            return self.balance

def safe_increment(thread_name, iterations):
    """Safe increment with lock synchronization"""
    global shared_counter, counter_lock

    for i in range(iterations):
        with counter_lock:

            current_value = shared_counter
            time.sleep(0.0001)
            shared_counter = current_value + 1

        if i % 1000 == 0:
            print(f"{thread_name}: iteration {i}, counter = {shared_counter}")

def demonstrate_thread_safety():
    """Demonstrate thread-safe operations using locks"""
    global shared_counter
    shared_counter = 0

    print("=== Thread Safety with Locks ===")
    print("Running safe increment with multiple threads...")

    iterations = 5000
    num_threads = 3

    threads = []
    start_time = time.time()


    for i in range(num_threads):
        thread = threading.Thread(
            target=safe_increment,
            args=(f"Thread-{i+1}", iterations)
        )
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()

    end_time = time.time()
    expected_value = iterations * num_threads

    print(f"\nResults:")
    print(f"Expected counter value: {expected_value}")
    print(f"Actual counter value: {shared_counter}")
    print(f"Difference: {expected_value - shared_counter}")
    print(f"Execution time: {end_time - start_time:.2f} seconds")

    if shared_counter == expected_value:
        print("✅ Thread synchronization successful! Counter value is correct.")
    else:
        raise RuntimeError("Thread synchronization failed")

def bank_account_simulation():
    """Simulate concurrent bank account operations"""
    print("\n=== Bank Account Simulation ===")

    account = BankAccount(1000)
    print(f"Initial balance: ${account.get_balance()}")

    def customer_transactions(customer_name, account):
        """Simulate customer performing random transactions"""
        for i in range(5):
            operation = random.choice(['deposit', 'withdraw'])
            amount = random.randint(50, 200)

            if operation == 'deposit':
                account.deposit(amount, customer_name)
            else:
                account.withdraw(amount, customer_name)

            time.sleep(random.uniform(0.1, 0.3))


    customers = ['Alice', 'Bob', 'Charlie']
    threads = []

    for customer in customers:
        thread = threading.Thread(target=customer_transactions, args=(customer, account))
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()

    print(f"\nFinal balance: ${account.get_balance()}")
    print(f"Total transactions: {len(account.transaction_history)}")

def main():
    demonstrate_thread_safety()
    bank_account_simulation()

if __name__ == "__main__":
    main()
```

