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
