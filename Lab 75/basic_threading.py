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
