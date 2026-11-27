# Lab 77: Multiprocessing in Python - Introduction to Multiprocessing

Run independent worker processes, use spawn-compatible pools and queues, calculate factorials in parallel, and update a shared-memory NumPy array.

## Concept in Hinglish

Processes ki normal memory alag hoti hai. Queue data exchange karti hai aur shared_memory common array ke liye use hoti hai. Process workers module level par hain, taaki spawn unhe import kar sake. Chhoti calculations mein process startup ka cost speed benefit se zyada ho sakta hai.

## Run

From the repository root, enter this folder. Python 3.8+ is required; the recorded validation uses Python 3.12.14. A virtual environment is recommended for third-party packages.

```bash
cd "Lab 77"
python3 -m pip install -r requirements.txt
python3 basic_multiprocessing.py
python3 performance_comparison.py
python3 process_pool_demo.py
python3 queue_communication.py
python3 parallel_factorial.py
python3 advanced_multiprocessing.py
```

## Completion and corrections

- Completed advanced_multiprocessing.py with counters, NumPy shared memory, result checks and close/unlink cleanup.
- Moved starmap and queue workers to module level and explicitly used spawn contexts.
- Bounded process pools to at most four workers for factorial calculations.
- Collected large queue results before joining producers, avoiding the output-queue join deadlock.
- All factorial methods reject invalid inputs and compare actual results with math.factorial.
- The duration-based basic example demonstrates scheduling; use performance_comparison.py for equal fixed-work measurements.

## Validation

```bash
python3 -m unittest discover -v -p "test_lab77.py"
```

The committed [verification/](verification/) directory contains the recorded local run. From the repository root, `python3 tools/validate_labs75_82.py --smoke` reruns all eight labs and writes fresh logs to `validation-output/`. Timing values and intentional race outcomes can change between runs. Persistent servers and interactive clients are covered by owned-server integration tests rather than left running by the smoke runner.

## Files

| File | Role |
|---|---|
| [advanced_multiprocessing.py](advanced_multiprocessing.py) | Runnable example or imported lab component |
| [basic_multiprocessing.py](basic_multiprocessing.py) | Runnable example or imported lab component |
| [parallel_factorial.py](parallel_factorial.py) | Runnable example or imported lab component |
| [performance_comparison.py](performance_comparison.py) | Runnable example or imported lab component |
| [process_pool_demo.py](process_pool_demo.py) | Runnable example or imported lab component |
| [queue_communication.py](queue_communication.py) | Runnable example or imported lab component |

The [complete guide](LAB_GUIDE.md) contains every final source file with its context. Missing endings and incremental class fragments were independently completed from the supplied lab requirements; these files are the runnable final implementation.
