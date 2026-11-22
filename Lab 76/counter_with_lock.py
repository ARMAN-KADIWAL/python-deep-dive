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
