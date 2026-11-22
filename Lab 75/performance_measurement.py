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
