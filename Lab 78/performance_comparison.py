import asyncio
import json
import multiprocessing as mp
import sys
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from itertools import repeat
from pathlib import Path


def simulate_io_sync(task_id, duration):
    time.sleep(duration)
    return task_id


async def simulate_io_async(task_id, duration):
    await asyncio.sleep(duration)
    return task_id


def simulate_cpu_work(task_id, iterations):
    total = 0
    for i in range(iterations):
        total += i * i
    return task_id, total


def run_pool(executor_type, function, num_tasks, argument):
    options = {"max_workers": min(5, num_tasks)}
    if executor_type is ProcessPoolExecutor:
        options["mp_context"] = mp.get_context("spawn")
    with executor_type(**options) as executor:
        return list(executor.map(function, range(num_tasks), repeat(argument)))


async def run_async_io(num_tasks, duration):
    return await asyncio.gather(*(
        simulate_io_async(i, duration) for i in range(num_tasks)
    ))


async def run_async_cpu(num_tasks, iterations):
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor(
        max_workers=min(5, num_tasks), mp_context=mp.get_context("spawn")
    ) as executor:
        return await asyncio.gather(*(
            loop.run_in_executor(executor, simulate_cpu_work, i, iterations)
            for i in range(num_tasks)
        ))


def measure_sync(name, operation, expected):
    started = time.perf_counter()
    results = operation()
    elapsed = time.perf_counter() - started
    if results != expected:
        raise RuntimeError(f"Incorrect results: {name}")
    print(f"{name}: {elapsed:.3f}s | verified=True")
    return {"seconds": elapsed, "verified": True}


async def measure_async(name, operation, expected):
    started = time.perf_counter()
    results = await operation
    elapsed = time.perf_counter() - started
    if results != expected:
        raise RuntimeError(f"Incorrect results: {name}")
    print(f"{name}: {elapsed:.3f}s | verified=True")
    return {"seconds": elapsed, "verified": True}


async def main():
    io_tasks, duration = 5, 1.0
    cpu_tasks, iterations = 4, 1_000_000
    expected_io = list(range(io_tasks))
    total = iterations * (iterations - 1) * (2 * iterations - 1) // 6
    expected_cpu = [(i, total) for i in range(cpu_tasks)]
    report = {"python": sys.version.split()[0], "io": {}, "cpu": {}}

    print("I/O COMPARISON: Five tasks, one second each")
    report["io"]["synchronous"] = measure_sync(
        "Synchronous I/O",
        lambda: [simulate_io_sync(i, duration) for i in range(io_tasks)], expected_io
    )
    report["io"]["asyncio"] = await measure_async(
        "Asyncio I/O", run_async_io(io_tasks, duration), expected_io
    )
    report["io"]["threading"] = measure_sync(
        "Threading I/O",
        lambda: run_pool(ThreadPoolExecutor, simulate_io_sync, io_tasks, duration),
        expected_io
    )
    report["io"]["multiprocessing"] = measure_sync(
        "Multiprocessing I/O",
        lambda: run_pool(ProcessPoolExecutor, simulate_io_sync, io_tasks, duration),
        expected_io
    )

    print("\nCPU COMPARISON: Four tasks, identical iteration counts")
    report["cpu"]["synchronous"] = measure_sync(
        "Synchronous CPU",
        lambda: [simulate_cpu_work(i, iterations) for i in range(cpu_tasks)],
        expected_cpu
    )
    report["cpu"]["threading"] = measure_sync(
        "Threading CPU",
        lambda: run_pool(ThreadPoolExecutor, simulate_cpu_work, cpu_tasks, iterations),
        expected_cpu
    )
    report["cpu"]["multiprocessing"] = measure_sync(
        "Multiprocessing CPU",
        lambda: run_pool(ProcessPoolExecutor, simulate_cpu_work, cpu_tasks, iterations),
        expected_cpu
    )
    report["cpu"]["asyncio_process_pool"] = await measure_async(
        "Asyncio + process pool CPU", run_async_cpu(cpu_tasks, iterations), expected_cpu
    )

    output = Path(__file__).resolve().parent / "benchmark_results.json"
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nReport saved: {output.name}")
    print("Process/thread startup and shutdown are included in timings.")
    print("Small CPU tasks may be slower with process startup overhead.")
    print("PASS: All eight benchmark results verified.")


if __name__ == "__main__":
    mp.freeze_support()
    asyncio.run(main())
