import multiprocessing as mp
import threading


def worker(first_lock, second_lock, barrier, name):
    with first_lock:
        print(f"{name}: first lock acquired", flush=True)
        barrier.wait()
        print(f"{name}: waiting for the other lock", flush=True)
        with second_lock:
            print(f"{name}: both locks acquired", flush=True)


def run_deadlock_scenario():
    lock1, lock2 = threading.Lock(), threading.Lock()
    barrier = threading.Barrier(2)
    threads = [
        threading.Thread(target=worker, args=(lock1, lock2, barrier, "Worker 1")),
        threading.Thread(target=worker, args=(lock2, lock1, barrier, "Worker 2")),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def demonstrate_deadlock(timeout=3):
    process = mp.get_context("spawn").Process(target=run_deadlock_scenario)
    process.start()
    try:
        process.join(timeout)
        if process.is_alive():
            print("DEADLOCK DETECTED: terminating only the isolated demonstration process.")
            return True
        raise RuntimeError("The intentional deadlock did not occur")
    finally:
        if process.is_alive():
            process.terminate()
        process.join()
        process.close()


def main():
    demonstrate_deadlock()
    print("PASS: Intentional deadlock detected and isolated process cleaned up.")


if __name__ == "__main__":
    mp.freeze_support()
    main()
