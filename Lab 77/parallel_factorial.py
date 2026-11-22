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
