# Lab 74 — Full TDD Cycle: Sorting

The full step-by-step course material is in [LAB_GUIDE.md](LAB_GUIDE.md).

## Linux quick start

```bash
cd 'Lab 74'
python3 -m unittest discover -v -p 'test_*.py'
python3 run_all_tests.py
python3 demo_sorting.py
```

The final `sorting.py` implements ascending, descending and flexible sorting.
Tests cover empty input, duplicates, negative numbers, invalid types and
large datasets. The source guide shows intermediate failing versions for
TDD; the submitted Python files represent the final working implementation.
