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
