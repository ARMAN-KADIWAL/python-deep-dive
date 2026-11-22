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
