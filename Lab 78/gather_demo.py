import argparse
import asyncio
import json
import random
import tempfile
import time
from pathlib import Path

import aiohttp


async def simple_task(name, duration):
    await asyncio.sleep(duration)
    return name


async def gather_example_1():
    started = time.perf_counter()
    results = await asyncio.gather(
        simple_task("A", 2),
        simple_task("B", 1),
        simple_task("C", 3),
        simple_task("D", 1.5),
    )
    if results != ["A", "B", "C", "D"]:
        raise RuntimeError("gather result order is incorrect")
    print(f"Basic gather results: {results}")
    print(f"Elapsed: {time.perf_counter() - started:.2f}s")


async def download_url(session, url, name):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            content = await response.read()
            return {"name": name, "status": response.status, "bytes": len(content)}
    except (aiohttp.ClientError, asyncio.TimeoutError) as error:
        return {"name": name, "status": "error", "error": str(error)}


async def gather_example_2(base_url):
    endpoints = [("delay/1", "Delay 1s"), ("delay/2", "Delay 2s"),
                 ("json", "JSON data"), ("uuid", "UUID generator")]
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        results = await asyncio.gather(*(
            download_url(session, f"{base_url.rstrip('/')}/{path}", name)
            for path, name in endpoints
        ))
    print("HTTP results:")
    print(json.dumps(results, indent=2))
    return all(item["status"] == 200 for item in results)


async def simulate_database_query(name, delay):
    await asyncio.sleep(delay)
    return {"query": name, "rows": random.randint(10, 100)}


async def gather_example_3():
    results = await asyncio.gather(
        simulate_database_query("SELECT users", 1.5),
        simulate_database_query("SELECT products", 2),
        simulate_database_query("SELECT orders", 1),
    )
    print("Database simulation:")
    print(json.dumps(results, indent=2))


def write_and_read_file(path, content):
    path.write_text(content, encoding="utf-8")
    return path.read_text(encoding="utf-8")


async def gather_example_4():
    loop = asyncio.get_running_loop()
    with tempfile.TemporaryDirectory(prefix="asyncio-lab-") as directory:
        expected = [f"Contents of file {i}" for i in range(3)]
        results = await asyncio.gather(*(
            loop.run_in_executor(
                None, write_and_read_file, Path(directory) / f"file_{i}.txt", text
            )
            for i, text in enumerate(expected)
        ))
    if results != expected:
        raise RuntimeError("File read/write verification failed")
    print("PASS: Three real files written, read and cleaned up.")


async def main(base_url):
    await gather_example_1()
    http_ok = await gather_example_2(base_url)
    await gather_example_3()
    await gather_example_4()
    if not http_ok:
        raise RuntimeError("HTTP requests failed; check the URL and network access")
    print("PASS: Gather, HTTP, database simulation and real file I/O completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="https://httpbin.org")
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()
    if args.offline:
        from http_fixture import local_site
        with local_site() as base_url:
            asyncio.run(main(base_url))
    else:
        asyncio.run(main(args.base_url))
