# Lab 73 — Test-Driven Development: Factorial

Read [LAB_GUIDE.md](LAB_GUIDE.md) to follow the Red → Green → Refactor cycle.

## Linux quick start

```bash
cd 'Lab 73'
python3 -m unittest discover -v -p 'test_*.py'
python3 demo.py
```

The committed files are the final working factorial and its six tests.
Expected test result: `Ran 6 tests` and `OK`.

The guide intentionally begins with failing tests; they pass once the final
`factorial.py` implementation is present. The recursive approach in this lab
is intended for small inputs and can hit Python's recursion limit for large n.
