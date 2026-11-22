# Lab 76: Thread Synchronization - Managing Shared Resources with Locks

Observe lost updates, protect a shared counter, demonstrate a controlled deadlock, compare prevention strategies and transfer items through a bounded condition-variable buffer.

## Concept in Hinglish

Read, modify aur write milkar ek critical section banate hain. Join sirf wait karta hai; lock shared data protect karta hai. Deadlock demo apne isolated child process mein atakta hai aur parent usi child ko time limit par clean karta hai. Timeout se operation abandon ho sakta hai, isliye completion counts alag dikhte hain.

## Run

From the repository root, enter this folder. Python 3.8+ is required; the recorded validation uses Python 3.12.14. A virtual environment is recommended for third-party packages.

```bash
cd "Lab 76"
python3 counter_without_lock.py
python3 counter_with_lock.py
python3 lock_comparison.py
python3 deadlock_demo.py
python3 deadlock_prevention.py
python3 producer_consumer.py
```

These examples use the Python standard library.

## Completion and corrections

- The intentional deadlock runs inside an owned child process and is terminated safely after detection; no broad process-kill command is needed.
- Timeout/try-lock examples report abandoned operations honestly and check that no locks remain held.
- Bounded-buffer capacity is validated; both lock-management counter styles are tested.
- Artificial sleeps inside critical sections are deliberate demonstrations, not a general claim about lock overhead.

## Validation

```bash
python3 -m unittest discover -v -p "test_lab76.py"
```

The committed [verification/](verification/) directory contains the recorded local run. From the repository root, `python3 validate_labs75_82.py --smoke` reruns all eight labs and writes fresh logs to `validation-output/`. Timing values and intentional race outcomes can change between runs. Persistent servers and interactive clients are covered by owned-server integration tests rather than left running by the smoke runner.

## Files

| File | Role |
|---|---|
| [counter_with_lock.py](counter_with_lock.py) | Runnable example or imported lab component |
| [counter_without_lock.py](counter_without_lock.py) | Runnable example or imported lab component |
| [deadlock_demo.py](deadlock_demo.py) | Runnable example or imported lab component |
| [deadlock_prevention.py](deadlock_prevention.py) | Runnable example or imported lab component |
| [lock_comparison.py](lock_comparison.py) | Runnable example or imported lab component |
| [producer_consumer.py](producer_consumer.py) | Runnable example or imported lab component |

The [complete guide](LAB_GUIDE.md) contains every final source file with its context. Missing endings and incremental class fragments were independently completed from the supplied lab requirements; these files are the runnable final implementation.
