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
