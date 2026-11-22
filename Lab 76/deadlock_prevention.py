import queue
import threading
import time


def worker_ordered_locking(first_lock, second_lock):
    with first_lock:
        with second_lock:
            time.sleep(0.02)
            return True


def worker_timeout_approach(first_lock, second_lock):
    if not first_lock.acquire(timeout=0.2):
        return False
    try:
        time.sleep(0.01)
        if not second_lock.acquire(timeout=0.2):
            return False
        try:
            return True
        finally:
            second_lock.release()
    finally:
        first_lock.release()


def worker_try_lock_approach(first_lock, second_lock):
    for _ in range(20):
        if first_lock.acquire(blocking=False):
            try:
                if second_lock.acquire(blocking=False):
                    try:
                        return True
                    finally:
                        second_lock.release()
            finally:
                first_lock.release()
        time.sleep(0.01)
    return False


def run_strategy(strategy, reverse=False):
    lock1, lock2 = threading.Lock(), threading.Lock()
    outcomes = queue.Queue()

    def run(first, second):
        try:
            outcomes.put(strategy(first, second))
        except Exception as error:
            outcomes.put(error)

    second_pair = (lock2, lock1) if reverse else (lock1, lock2)
    threads = [threading.Thread(target=run, args=(lock1, lock2)), threading.Thread(target=run, args=second_pair)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=2)
    if any(thread.is_alive() for thread in threads):
        raise RuntimeError("Prevention strategy left a worker blocked")
    results = [outcomes.get_nowait() for _ in threads]
    for result in results:
        if isinstance(result, Exception):
            raise result
    print(f"{strategy.__name__}: {sum(results)}/2 operations completed; {results.count(False)} abandoned safely")
    if lock1.locked() or lock2.locked():
        raise RuntimeError("A prevention strategy leaked a lock")
    return results


def main():
    if run_strategy(worker_ordered_locking) != [True, True]:
        raise RuntimeError("Ordered locking failed to complete both operations")
    run_strategy(worker_timeout_approach, reverse=True)
    run_strategy(worker_try_lock_approach, reverse=True)
    print("PASS: All strategies returned without deadlock or leaked locks.")
    print("Timeout/retry approaches can abandon an operation; completion counts are shown above.")


if __name__ == "__main__":
    main()
