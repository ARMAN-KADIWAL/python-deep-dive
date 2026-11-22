# Lab 77: Multiprocessing in Python - Introduction to Multiprocessing — Complete Guide

Run independent worker processes, use spawn-compatible pools and queues, calculate factorials in parallel, and update a shared-memory NumPy array.

Processes ki normal memory alag hoti hai. Queue data exchange karti hai aur shared_memory common array ke liye use hoti hai. Process workers module level par hain, taaki spawn unhe import kar sake. Chhoti calculations mein process startup ka cost speed benefit se zyada ho sakta hai.

Follow [README.md](README.md) for setup, commands, ports and validation. These are the complete final modules, not the intermediate/truncated snippets from the supplied handout.

## advanced_multiprocessing.py

```python
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
```

## basic_multiprocessing.py

```python
import multiprocessing
import threading
import time
import os

def cpu_bound_task(name, duration):
    """Simulate a CPU-intensive task"""
    print(f'Process {name} (PID: {os.getpid()}) starting...')
    start_time = time.time()
    count = 0
    while time.time() - start_time < duration:
        count += 1
    print(f'Process {name} (PID: {os.getpid()}) completed. Count: {count}')
    return count

def run_sequential():
    """Run tasks sequentially"""
    print('=== Sequential Execution ===')
    start_time = time.time()
    cpu_bound_task('Task1', 2)
    cpu_bound_task('Task2', 2)
    cpu_bound_task('Task3', 2)
    end_time = time.time()
    print(f'Sequential execution time: {end_time - start_time:.2f} seconds\n')

def run_multiprocessing():
    """Run tasks using multiprocessing"""
    print('=== Multiprocessing Execution ===')
    start_time = time.time()
    processes = []
    for i in range(1, 4):
        process = multiprocessing.get_context("spawn").Process(target=cpu_bound_task, args=(f'Task{i}', 2))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    end_time = time.time()
    print(f'Multiprocessing execution time: {end_time - start_time:.2f} seconds\n')
if __name__ == '__main__':
    print('Multiprocessing vs Sequential Execution Demo')
    print('=' * 50)
    run_sequential()
    run_multiprocessing()
```

## parallel_factorial.py

```python
import math
import multiprocessing as mp
import time
from functools import reduce
from operator import mul
from queue import Empty


def validate(n, num_processes):
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    if num_processes is None:
        num_processes = min(4, mp.cpu_count())
    if not isinstance(num_processes, int) or isinstance(num_processes, bool):
        raise TypeError("num_processes must be an integer")
    if num_processes < 1:
        raise ValueError("num_processes must be positive")
    return min(num_processes, max(1, n), 4)


def split_ranges(n, count):
    return [(i * n // count + 1, (i + 1) * n // count) for i in range(count)]


def calculate_partial_factorial(start, end):
    return math.prod(range(start, end + 1))


def sequential_factorial(n):
    validate(n, None)
    return math.factorial(n)


def parallel_factorial(n, num_processes=None):
    count = validate(n, num_processes)
    if n < 2:
        return 1
    with mp.get_context("spawn").Pool(processes=count) as pool:
        partial = pool.starmap(calculate_partial_factorial, split_ranges(n, count))
    return reduce(mul, partial, 1)


def factorial_queue_worker(work, output):
    total = 1
    while True:
        item = work.get()
        if item is None:
            break
        total *= calculate_partial_factorial(*item)
    output.put(total)


def optimized_parallel_factorial(n, num_processes=None):
    count = validate(n, num_processes)
    if n < 2:
        return 1
    context = mp.get_context("spawn")
    work, output = context.Queue(), context.Queue()
    workers = [context.Process(target=factorial_queue_worker, args=(work, output)) for _ in range(count)]
    for process in workers:
        process.start()
    try:
        for bounds in split_ranges(n, count):
            work.put(bounds)
        for _ in workers:
            work.put(None)
        try:
            partial = [output.get(timeout=30) for _ in workers]
        except Empty as error:
            raise RuntimeError("A factorial worker did not return a result") from error
        for process in workers:
            process.join(timeout=5)
            if process.is_alive() or process.exitcode != 0:
                raise RuntimeError("A factorial worker did not exit successfully")
        return reduce(mul, partial, 1)
    finally:
        for process in workers:
            if process.is_alive():
                process.terminate()
            process.join()
            process.close()
        work.close()
        work.join_thread()
        output.close()
        output.join_thread()


def benchmark_factorial_methods(n):
    expected = math.factorial(n)
    results = {}
    methods = [("math.factorial", sequential_factorial), ("Process pool", parallel_factorial), ("Queue-based", optimized_parallel_factorial)]
    for name, function in methods:
        started = time.perf_counter()
        actual = function(n)
        elapsed = time.perf_counter() - started
        if actual != expected:
            raise RuntimeError(f"Incorrect factorial from {name}")
        results[name] = elapsed
        print(f"{n}! | {name}: {elapsed:.4f}s | verified=True")
    return results


def main():
    for n in (10, 100, 1000):
        benchmark_factorial_methods(n)
    print("PASS: All factorial methods agree with math.factorial.")
    print("The queue-based method name is retained from the handout; it is not guaranteed to be faster.")


if __name__ == "__main__":
    mp.freeze_support()
    main()
```

## performance_comparison.py

```python
import multiprocessing as mp
import time
from concurrent.futures import ThreadPoolExecutor


def cpu_intensive_task(n):
    return sum(i * i for i in range(n))


def io_bound_task(duration):
    time.sleep(duration)
    return duration


def measure(name, function, values, use_processes, expected):
    started = time.perf_counter()
    if use_processes:
        with mp.get_context("spawn").Pool(processes=min(4, len(values))) as pool:
            results = pool.map(function, values)
    else:
        with ThreadPoolExecutor(max_workers=min(4, len(values))) as pool:
            results = list(pool.map(function, values))
    elapsed = time.perf_counter() - started
    if results != expected:
        raise RuntimeError(f"Incorrect results: {name}")
    print(f"{name}: {elapsed:.4f}s; results verified")
    return elapsed


def main():
    count, iterations = 4, 1_000_000
    expected = iterations * (iterations - 1) * (2 * iterations - 1) // 6
    measure("CPU processes", cpu_intensive_task, [iterations] * count, True, [expected] * count)
    measure("CPU threads", cpu_intensive_task, [iterations] * count, False, [expected] * count)
    measure("I/O processes", io_bound_task, [1] * count, True, [1] * count)
    measure("I/O threads", io_bound_task, [1] * count, False, [1] * count)
    print("Startup and shutdown are included; processes are not guaranteed to be faster for small tasks.")


if __name__ == "__main__":
    mp.freeze_support()
    main()
```

## process_pool_demo.py

```python
def multiply_task(x, y, task_name):
    """Task that takes multiple arguments"""
    process_id = os.getpid()
    result = x * y
    print(f'Process {process_id} - {task_name}: {x} * {y} = {result}')
    return result
import multiprocessing
import time
import random
import os

def worker_task(task_id):
    """Simulate work being done by a worker process"""
    process_id = os.getpid()
    work_time = random.uniform(0.05, 0.15)
    print(f'Worker {process_id} starting task {task_id}')
    time.sleep(work_time)
    result = task_id ** 2
    print(f'Worker {process_id} completed task {task_id} in {work_time:.2f}s, result: {result}')
    return {'task_id': task_id, 'process_id': process_id, 'work_time': work_time, 'result': result}

def demonstrate_pool_map():
    """Demonstrate Pool.map() functionality"""
    print('=== Pool.map() Demonstration ===')
    tasks = list(range(1, 9))
    pool_size = 4
    print(f'Processing {len(tasks)} tasks with {pool_size} worker processes')
    start_time = time.time()
    with multiprocessing.get_context("spawn").Pool(processes=pool_size) as pool:
        results = pool.map(worker_task, tasks)
    end_time = time.time()
    print(f'\nAll tasks completed in {end_time - start_time:.2f} seconds')
    print('Results summary:')
    for result in results:
        print(f"  Task {result['task_id']}: {result['result']} (Process {result['process_id']})")

def demonstrate_pool_apply_async():
    """Demonstrate Pool.apply_async() for more control"""
    print('\n=== Pool.apply_async() Demonstration ===')
    tasks = list(range(1, 6))
    pool_size = 3
    print(f'Processing {len(tasks)} tasks asynchronously with {pool_size} workers')
    start_time = time.time()
    with multiprocessing.get_context("spawn").Pool(processes=pool_size) as pool:
        async_results = []
        for task_id in tasks:
            async_result = pool.apply_async(worker_task, (task_id,))
            async_results.append(async_result)
        results = []
        for async_result in async_results:
            result = async_result.get()
            results.append(result)
            print(f"Collected result for task {result['task_id']}")
    end_time = time.time()
    print(f'\nAll async tasks completed in {end_time - start_time:.2f} seconds')

def demonstrate_pool_starmap():
    """Demonstrate Pool.starmap() for multiple arguments"""
    print('\n=== Pool.starmap() Demonstration ===')
    task_args = [(2, 3, 'Task A'), (4, 5, 'Task B'), (6, 7, 'Task C'), (8, 9, 'Task D'), (10, 11, 'Task E')]
    with multiprocessing.get_context("spawn").Pool(processes=3) as pool:
        results = pool.starmap(multiply_task, task_args)
    print(f'Starmap results: {results}')

def main():
    print('Process Pool Demonstrations')
    print('=' * 50)
    demonstrate_pool_map()
    demonstrate_pool_apply_async()
    demonstrate_pool_starmap()
if __name__ == '__main__':
    main()
```

## queue_communication.py

```python
import multiprocessing as mp
from queue import Empty


def producer(work, producer_id, num_items):
    for item in range(num_items):
        work.put((producer_id, item))


def consumer(work, results):
    while True:
        item = work.get()
        if item is None:
            return
        results.put(item)


def worker_with_results(work, results):
    while True:
        task = work.get()
        if task is None:
            return
        task_id, number = task
        results.put((task_id, number * number))


def collect(results, count):
    try:
        return [results.get(timeout=15) for _ in range(count)]
    except Empty as error:
        raise RuntimeError("A worker failed to return its expected result") from error


def finish(processes, queues):
    failed = []
    for process in processes:
        process.join(timeout=5)
        if process.is_alive():
            process.terminate()
            process.join()
            failed.append("worker did not finish")
        elif process.exitcode != 0:
            failed.append(f"exit code {process.exitcode}")
        process.close()
    for channel in queues:
        channel.close()
        channel.join_thread()
    if failed:
        raise RuntimeError(", ".join(failed))


def demonstrate_basic_queue():
    context = mp.get_context("spawn")
    work, results = context.Queue(), context.Queue()
    producers = [context.Process(target=producer, args=(work, i, 3)) for i in range(2)]
    consumers = [context.Process(target=consumer, args=(work, results)) for _ in range(2)]
    processes = producers + consumers
    for process in processes:
        process.start()
    try:
        for process in producers:
            process.join()
        for _ in consumers:
            work.put(None)
        actual = collect(results, 6)
        expected = [(i, j) for i in range(2) for j in range(3)]
        if sorted(actual) != expected:
            raise RuntimeError("Queue lost or duplicated a produced item")
        print("PASS: Six produced items consumed exactly once.")
        return actual
    finally:
        finish(processes, (work, results))


def demonstrate_bidirectional_queue():
    context = mp.get_context("spawn")
    work, results = context.Queue(), context.Queue()
    tasks = [(i, number) for i, number in enumerate((5, 10, 15, 20, 25))]
    workers = [context.Process(target=worker_with_results, args=(work, results)) for _ in range(3)]
    for process in workers:
        process.start()
    try:
        for task in tasks:
            work.put(task)
        for _ in workers:
            work.put(None)
        actual = collect(results, len(tasks))
        if sorted(actual) != [(i, n * n) for i, n in tasks]:
            raise RuntimeError("Bidirectional queue returned incorrect results")
        print(f"PASS: Bidirectional queue results: {sorted(actual)}")
        return actual
    finally:
        finish(workers, (work, results))


def main():
    demonstrate_basic_queue()
    demonstrate_bidirectional_queue()


if __name__ == "__main__":
    mp.freeze_support()
    main()
```

