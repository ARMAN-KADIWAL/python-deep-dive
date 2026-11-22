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
