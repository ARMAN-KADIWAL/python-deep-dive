import asyncio
import time


async def slow_operation_async(name, duration):
    print(f"Starting {name}...", flush=True)
    await asyncio.sleep(duration)
    print(f"Completed {name} after {duration} seconds", flush=True)
    return f"Result from {name}"


async def main():
    started = time.perf_counter()
    results = await asyncio.gather(
        slow_operation_async("Task 1", 2),
        slow_operation_async("Task 2", 3),
        slow_operation_async("Task 3", 1),
    )
    print(f"Total execution time: {time.perf_counter() - started:.2f} seconds")
    print(f"Results: {results}")


if __name__ == "__main__":
    asyncio.run(main())
