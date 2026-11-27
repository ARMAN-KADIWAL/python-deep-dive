# Lab 75: Introduction to Threading - Basic Threading in Python

Create and join threads, compare equal CPU workloads, coordinate shared data with locks, run a real shared work queue, and inspect thread lifecycles.

## Concept in Hinglish

Thread ek process ka worker hai. I/O wait ke dauraan doosra thread aage badh sakta hai. Shared counter ya bank balance update karte waqt same lock use karo. Worker pool mein sab workers ek common queue se jobs lete hain; har worker ko jobs ki alag copy nahi milti.

## Run

From the repository root, enter this folder. Python 3.8+ is required; the recorded validation uses Python 3.12.14. A virtual environment is recommended for third-party packages.

```bash
cd "Lab 75"
python3 basic_threading.py
python3 sequential_vs_concurrent.py
python3 gil_demonstration.py
python3 performance_measurement.py
python3 advanced_threading.py
python3 thread_lifecycle.py
python3 race_condition_demo.py
python3 thread_synchronization.py
python3 advanced_locks.py
python3 thread_monitoring.py
```

These examples use the Python standard library.

## Completion and corrections

- Reconstructed the missing thread_monitoring.py ending.
- Replaced copied per-worker task lists with one shared Queue, verifying exactly-once processing.
- Protected bank transactions, validated positive amounts and guaranteed resource release.
- The Fibonacci demonstration uses n=30 so the default classroom run stays short; it still compares the same workload in both approaches.
- Race-condition output is intentionally incorrect and timing-dependent. GIL observations refer to ordinary GIL-enabled CPython, not every Python build.

## Validation

```bash
python3 -m unittest discover -v -p "test_lab75.py"
```

The committed [verification/](verification/) directory contains the recorded local run. From the repository root, `python3 tools/validate_labs75_82.py --smoke` reruns all eight labs and writes fresh logs to `validation-output/`. Timing values and intentional race outcomes can change between runs. Persistent servers and interactive clients are covered by owned-server integration tests rather than left running by the smoke runner.

## Files

| File | Role |
|---|---|
| [advanced_locks.py](advanced_locks.py) | Runnable example or imported lab component |
| [advanced_threading.py](advanced_threading.py) | Runnable example or imported lab component |
| [basic_threading.py](basic_threading.py) | Runnable example or imported lab component |
| [gil_demonstration.py](gil_demonstration.py) | Runnable example or imported lab component |
| [performance_measurement.py](performance_measurement.py) | Runnable example or imported lab component |
| [race_condition_demo.py](race_condition_demo.py) | Runnable example or imported lab component |
| [sequential_vs_concurrent.py](sequential_vs_concurrent.py) | Runnable example or imported lab component |
| [thread_lifecycle.py](thread_lifecycle.py) | Runnable example or imported lab component |
| [thread_monitoring.py](thread_monitoring.py) | Runnable example or imported lab component |
| [thread_synchronization.py](thread_synchronization.py) | Runnable example or imported lab component |

The [complete guide](LAB_GUIDE.md) contains every final source file with its context. Missing endings and incremental class fragments were independently completed from the supplied lab requirements; these files are the runnable final implementation.
