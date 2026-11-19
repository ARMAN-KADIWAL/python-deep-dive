# Lab 70 — Unit Testing with `unittest`

The original guide is preserved in [LAB_GUIDE.md](LAB_GUIDE.md), with its
previously truncated troubleshooting and conclusion sections completed.

## Linux quick start

```bash
cd 'Lab 70'
python3 --version
python3 -m unittest discover -v -p 'test_*.py'
python3 manual_test.py
python3 test_suite.py
```

Includes final `arithmetic_operations.py`, basic and refactored unit tests,
assertion examples, parameterized tests and a factorial TDD example.
The guide's **red phase** intentionally describes earlier test failures;
these files contain the final **green phase** implementations.

No third-party packages are required for the tests. `coverage` is optional.
