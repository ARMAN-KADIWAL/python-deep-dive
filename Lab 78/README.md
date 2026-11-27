# Lab 78: Asynchronous Programming with asyncio - Introduction to Asyncio

Learn coroutines, async/await, gather, task scheduling, callbacks, error handling, actual HTTP/file operations and I/O versus CPU benchmarks.

## Concept in Hinglish

Asyncio ek event-loop thread mein ready tasks chalata hai. Pending I/O par await karne se doosre tasks ko chance milta hai. CPU loop ke aage async likh dene se woh non-blocking nahi banta. Gather results input order mein deta hai; as_completed ready results completion order mein deta hai.

## Run

From the repository root, enter this folder. Python 3.8+ is required; the recorded validation uses Python 3.12.14. A virtual environment is recommended for third-party packages.

```bash
cd "Lab 78"
python3 -m pip install -r requirements.txt
python3 sync_example.py
python3 async_example.py
python3 coroutines_demo.py
python3 async_error_handling.py
python3 gather_demo.py --offline
python3 concurrency_patterns.py
python3 event_loop_demo.py
python3 event_loop_debug.py
python3 performance_comparison.py
```

Offline mode uses actual HTTP requests against a controlled local server and needs no public API. To test the public example, omit `--offline`; this requires access to https://httpbin.org. A public HTTP/network failure is reported as a failure.

## Completion and corrections

- Completed performance_comparison.py and verified every benchmark result.
- Fixed random import scope and enabled the HTTP example with status checks and timeouts.
- Added actual file read/write through an executor and consistent sequential/concurrent inputs.
- Used a process executor for pure-Python CPU calculations and retained an explicitly labelled blocking demo.
- Offline fixtures exercise real local HTTP; public website availability is not implied by those checks.

## Validation

```bash
python3 -m unittest discover -v -p "test_lab78.py"
```

The committed [verification/](verification/) directory contains the recorded local run. From the repository root, `python3 tools/validate_labs75_82.py --smoke` reruns all eight labs and writes fresh logs to `validation-output/`. Timing values and intentional race outcomes can change between runs. Persistent servers and interactive clients are covered by owned-server integration tests rather than left running by the smoke runner.

## Files

| File | Role |
|---|---|
| [async_error_handling.py](async_error_handling.py) | Runnable example or imported lab component |
| [async_example.py](async_example.py) | Runnable example or imported lab component |
| [concurrency_patterns.py](concurrency_patterns.py) | Runnable example or imported lab component |
| [coroutines_demo.py](coroutines_demo.py) | Runnable example or imported lab component |
| [event_loop_debug.py](event_loop_debug.py) | Runnable example or imported lab component |
| [event_loop_demo.py](event_loop_demo.py) | Runnable example or imported lab component |
| [gather_demo.py](gather_demo.py) | Runnable example or imported lab component |
| [http_fixture.py](http_fixture.py) | Controlled real HTTP test server |
| [performance_comparison.py](performance_comparison.py) | Runnable example or imported lab component |
| [sync_example.py](sync_example.py) | Runnable example or imported lab component |

The [complete guide](LAB_GUIDE.md) contains every final source file with its context. Missing endings and incremental class fragments were independently completed from the supplied lab requirements; these files are the runnable final implementation.
