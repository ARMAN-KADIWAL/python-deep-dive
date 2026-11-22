import multiprocessing as mp
import time
from multiprocessing import shared_memory

import numpy as np


def worker_with_lock(lock, counter, iterations):
    for _ in range(iterations):
        with lock:
            value = counter.value
            time.sleep(0.001)
            counter.value = value + 1


def worker_without_lock(counter, iterations, barrier):
    barrier.wait(timeout=10)
    for _ in range(iterations):
        value = counter.value
        time.sleep(0.001)
        counter.value = value + 1


def run_processes(processes):
    started = []
    try:
        for process in processes:
            process.start()
            started.append(process)
        for process in started:
            process.join(timeout=20)
            if process.is_alive() or process.exitcode != 0:
                raise RuntimeError("Worker did not finish successfully")
    finally:
        for process in started:
            if process.is_alive():
                process.terminate()
            process.join()
            process.close()


def demonstrate_locks():
    context = mp.get_context("spawn")
    safe = context.Value("i", 0)
    lock = context.Lock()
    run_processes([
        context.Process(target=worker_with_lock, args=(lock, safe, 5))
        for _ in range(3)
    ])
    if safe.value != 15:
        raise RuntimeError("Locked counter is incorrect")
    print(f"Counter with lock: {safe.value}; expected: 15")

    unsafe = context.Value("i", 0)
    barrier = context.Barrier(3)
    run_processes([
        context.Process(target=worker_without_lock, args=(unsafe, 5, barrier))
        for _ in range(3)
    ])
    print(f"Counter without lock: {unsafe.value}; expected: 15")
    print("The unsafe result depends on scheduling; a correct run does not prove safety.")
    return safe.value, unsafe.value


def shared_array_worker(name, shape, dtype, start, end):
    memory = shared_memory.SharedMemory(name=name)
    array = None
    try:
        array = np.ndarray(shape, dtype=dtype, buffer=memory.buf)
        array[start:end] = array[start:end] ** 2
    finally:
        array = None
        memory.close()


def demonstrate_shared_memory():
    context = mp.get_context("spawn")
    original = np.arange(1, 11, dtype=np.int64)
    memory = shared_memory.SharedMemory(create=True, size=original.nbytes)
    shared = None
    try:
        shared = np.ndarray(original.shape, dtype=original.dtype, buffer=memory.buf)
        shared[:] = original
        run_processes([
            context.Process(
                target=shared_array_worker,
                args=(memory.name, original.shape, original.dtype, i * 10 // 3, (i + 1) * 10 // 3),
            )
            for i in range(3)
        ])
        result = shared.copy()
        if not np.array_equal(result, original ** 2):
            raise RuntimeError("Shared-memory result is incorrect")
        print(f"Shared array: {result.tolist()}")
        return result.tolist()
    finally:
        shared = None
        try:
            memory.close()
        finally:
            memory.unlink()


def main():
    demonstrate_locks()
    demonstrate_shared_memory()
    print("PASS: Counters and shared memory verified; resources cleaned up.")


if __name__ == "__main__":
    mp.freeze_support()
    main()
