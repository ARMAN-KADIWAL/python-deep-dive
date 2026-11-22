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
