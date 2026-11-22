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
