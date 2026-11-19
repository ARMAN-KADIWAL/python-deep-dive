# Lab 72 — Advanced IDE Debugging

The source lesson [LAB_GUIDE.md](LAB_GUIDE.md) describes VS Code breakpoints,
call stacks, watches and conditional breakpoints on Linux.

## Why two sets of files?

- `intentional_bugs/`: Original broken examples for debugger exercises,
  including a **genuine infinite loop** and runaway recursion. **Do not run
  `infinite_loop_demo.py` unattended**; stop debugging with Ctrl+C/Stop.
- `solutions/`: Corrected versions of the same exercises, plus tests.

## Linux quick start

```bash
cd 'Lab 72'
python3 -m unittest discover -v -p 'test_*.py'
python3 solutions/data_processor_fixed.py
python3 solutions/threading_fixed.py
```

Python's standard library is sufficient for these runnable examples.
The VS Code GUI exercises need a graphical VS Code installation; on a
terminal-only cloud VM, use `python3 -m pdb` to inspect the example scripts.
