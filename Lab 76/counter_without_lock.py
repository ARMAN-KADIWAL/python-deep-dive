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
