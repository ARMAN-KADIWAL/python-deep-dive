# Lab 78: Asynchronous Programming with asyncio - Introduction to Asyncio — Complete Guide

Learn coroutines, async/await, gather, task scheduling, callbacks, error handling, actual HTTP/file operations and I/O versus CPU benchmarks.

Asyncio ek event-loop thread mein ready tasks chalata hai. Pending I/O par await karne se doosre tasks ko chance milta hai. CPU loop ke aage async likh dene se woh non-blocking nahi banta. Gather results input order mein deta hai; as_completed ready results completion order mein deta hai.

Follow [README.md](README.md) for setup, commands, ports and validation. These are the complete final modules, not the intermediate/truncated snippets from the supplied handout.

## async_error_handling.py

```python
import asyncio


async def unreliable_operation(task_id):
    await asyncio.sleep(1)
    if task_id in {2, 5}:
        raise RuntimeError(f"Task {task_id} failed intentionally")
    return f"Task {task_id} completed successfully"


async def safe_operation(task_id):
    try:
        result = await unreliable_operation(task_id)
        print(f"SUCCESS: {result}")
        return {"task": task_id, "status": "success"}
    except RuntimeError as error:
        print(f"HANDLED: {error}")
        return {"task": task_id, "status": "failed"}


async def main():
    results = await asyncio.gather(*(safe_operation(i) for i in range(1, 6)))
    failed = [item["task"] for item in results if item["status"] == "failed"]
    if failed != [2, 5]:
        raise RuntimeError("Error handling verification failed")
    print(f"Final results: {results}")
    print("PASS: Task 2 and Task 5 failed safely; other tasks completed.")


if __name__ == "__main__":
    asyncio.run(main())
```

## async_example.py

```python
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
```

## concurrency_patterns.py

```python
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
```

## coroutines_demo.py

```python
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
```

## event_loop_debug.py

```python
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
```

## event_loop_demo.py

```python
import asyncio


async def task_with_callback(name, duration):
    print(f"Task {name} started")
    await asyncio.sleep(duration)
    print(f"Task {name} completed")
    return name


def callback_function(task):
    print(f"Done callback: {task.result()}")


async def event_loop_basics():
    loop = asyncio.get_running_loop()
    print(f"Current event loop: {loop}")
    loop.call_soon(print, "call_soon: Next loop iteration")
    loop.call_later(2, print, "call_later: About two seconds elapsed")

    tasks = [
        loop.create_task(task_with_callback("EventLoop1", 1)),
        loop.create_task(task_with_callback("EventLoop2", 2)),
    ]
    for task in tasks:
        task.add_done_callback(callback_function)
    await asyncio.gather(*tasks)


async def event_loop_scheduling():
    async def quick_task(name):
        print(f"Quick task {name}")
        return name

    tasks = []
    for i in range(3):
        tasks.append(asyncio.create_task(quick_task(f"Q{i}")))
        tasks.append(asyncio.create_task(task_with_callback(f"S{i}", 1)))
    results = await asyncio.gather(*tasks)
    print(f"Scheduled results: {results}")


async def event_loop_timing():
    loop = asyncio.get_running_loop()
    started = loop.time()
    await asyncio.sleep(1)
    print(f"Loop elapsed: {loop.time() - started:.2f}s")


async def main():
    await event_loop_basics()
    await event_loop_scheduling()
    await event_loop_timing()
    print("PASS: Event loop callbacks, scheduling and timing completed.")


if __name__ == "__main__":
    asyncio.run(main())
```

## gather_demo.py

```python
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
```

## http_fixture.py

```python
import threading
import time
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse


@contextmanager
def local_site(delay=0.03):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            path = urlparse(self.path).path
            status = 200
            if path.startswith("/delay/"):
                time.sleep(float(path.rsplit("/", 1)[1]))
            elif path == "/slow":
                time.sleep(0.2)
            else:
                time.sleep(delay)
            if path == "/flaky":
                with self.server.counter_lock:
                    self.server.flaky_count += 1
                    status = 503 if self.server.flaky_count == 1 else 200
            elif path.startswith("/status/"):
                status = int(path.rsplit("/", 1)[1])
            body = (
                f"<html><head><title>Fixture {path}</title></head><body>"
                "<h1>Local lab fixture</h1><p>First paragraph.</p>"
                "<p>Second paragraph.</p><a href='/next'>Next</a>"
                "<a href='/empty'></a><img src='/image.png'></body></html>"
            ).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    server.counter_lock = threading.Lock()
    server.flaky_count = 0
    thread = threading.Thread(target=lambda: server.serve_forever(poll_interval=0.05), daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
```

## performance_comparison.py

```python
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
```

## sync_example.py

```python
import time


def slow_operation(name, duration):
    print(f"Starting {name}...", flush=True)
    time.sleep(duration)
    print(f"Completed {name} after {duration} seconds", flush=True)
    return f"Result from {name}"


def main():
    started = time.perf_counter()
    results = [
        slow_operation("Task 1", 2),
        slow_operation("Task 2", 3),
        slow_operation("Task 3", 1),
    ]
    print(f"Total execution time: {time.perf_counter() - started:.2f} seconds")
    print(f"Results: {results}")


if __name__ == "__main__":
    main()
```

