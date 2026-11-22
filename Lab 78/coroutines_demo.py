import asyncio
import time


SOURCES = {
    "database": (1.0, {"users": 150, "products": 75}),
    "api": (1.5, {"weather": "sunny", "temperature": 25}),
    "file": (0.5, {"config": "loaded", "size": "2MB"}),
}


async def fetch_data(source_name):
    delay, data = SOURCES[source_name]
    print(f"Fetching {source_name}...")
    await asyncio.sleep(delay)
    return dict(data)


async def process_data(data, source_name):
    await asyncio.sleep(0.2)
    result = {"source": source_name, "fields": len(data)}
    print(f"Processed: {result}")
    return result


async def fetch_and_process(source_name):
    data = await fetch_data(source_name)
    return await process_data(data, source_name)


async def main():
    started = time.perf_counter()
    sequential = []
    for source_name in SOURCES:
        sequential.append(await fetch_and_process(source_name))
    print(f"Sequential time: {time.perf_counter() - started:.2f}s")

    started = time.perf_counter()
    tasks = [
        asyncio.create_task(fetch_and_process(name)) for name in SOURCES
    ]
    concurrent = await asyncio.gather(*tasks)
    print(f"Concurrent time: {time.perf_counter() - started:.2f}s")

    if sequential != concurrent:
        raise RuntimeError("Sequential and concurrent results differ")
    print("PASS: Same inputs and same results in both approaches.")


if __name__ == "__main__":
    asyncio.run(main())
