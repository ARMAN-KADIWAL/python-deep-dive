import asyncio
import logging
import multiprocessing as mp
import time
from concurrent.futures import ProcessPoolExecutor


def cpu_intensive_work(iterations):
    return sum(i * i for i in range(iterations))


async def cpu_bound_task(name, iterations):
    print(f"Blocking CPU task {name} starting")
    result = cpu_intensive_work(iterations)
    print(f"Blocking CPU task {name} finished")
    return result


async def io_bound_task(name, delay):
    await asyncio.sleep(delay)
    return name


async def monitor_event_loop():
    loop = asyncio.get_running_loop()
    loop.set_debug(True)
    loop.slow_callback_duration = 0.01

    started = time.perf_counter()
    results = await asyncio.gather(*(io_bound_task(f"IO{i}", 1) for i in range(3)))
    print(f"I/O results: {results}; {time.perf_counter() - started:.2f}s")

    print("Intentional blocking example: slow-task warnings may appear.")
    await asyncio.gather(*(cpu_bound_task(f"CPU{i}", 1_000_000) for i in range(3)))


async def proper_cpu_handling():
    loop = asyncio.get_running_loop()
    iterations = 1_000_000
    expected = iterations * (iterations - 1) * (2 * iterations - 1) // 6
    started = time.perf_counter()

    with ProcessPoolExecutor(max_workers=3, mp_context=mp.get_context("spawn")) as pool:
        results = await asyncio.gather(*(
            loop.run_in_executor(pool, cpu_intensive_work, iterations)
            for _ in range(3)
        ))

    if results != [expected] * 3:
        raise RuntimeError("CPU executor returned incorrect results")
    print(f"Process executor results: {results}")
    print(f"Executor elapsed: {time.perf_counter() - started:.2f}s")
    print("PASS: CPU calculations completed outside the event-loop process.")


async def main():
    await monitor_event_loop()
    await proper_cpu_handling()


if __name__ == "__main__":
    mp.freeze_support()
    logging.basicConfig(level=logging.WARNING)
    asyncio.run(main(), debug=True)
