import asyncio
import time


async def worker_task(name, duration):
    print(f"Starting {name}")
    await asyncio.sleep(duration)
    print(f"Completed {name}")
    return name


async def demonstrate(pattern):
    started = time.perf_counter()
    work = [worker_task("A", 2), worker_task("B", 1), worker_task("C", 3)]

    if pattern == "gather":
        results = await asyncio.gather(*work)
    elif pattern == "create_task":
        tasks = [asyncio.create_task(item) for item in work]
        results = [await task for task in tasks]
    elif pattern == "as_completed":
        results = []
        for item in asyncio.as_completed(work):
            result = await item
            print(f"Received: {result}")
            results.append(result)
    else:
        tasks = [asyncio.create_task(item) for item in work]
        done, pending = await asyncio.wait(tasks)
        results = [task.result() for task in done]
        if pending:
            raise RuntimeError("Unexpected pending tasks")

    if sorted(results) != ["A", "B", "C"]:
        raise RuntimeError("Missing or incorrect task result")
    print(f"{pattern}: {results}; {time.perf_counter() - started:.2f}s\n")


async def main():
    for pattern in ("gather", "create_task", "as_completed", "wait"):
        await demonstrate(pattern)
    print("PASS: All four concurrency patterns completed.")


if __name__ == "__main__":
    asyncio.run(main())
