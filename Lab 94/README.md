# Lab 94 — Inventory Management System

Final project demonstrating Product and Inventory models, Strategy pricing, Observer notifications, CSV reporting, and tests.

## Run

```bash
python3 src/main.py
python3 src/main.py --interactive
python3 -m pytest -q
```

Install development dependencies in a virtual environment with `python3 -m pip install -r requirements.txt`. The main application uses only Python's standard library. `black` and `flake8` are optional quality tools; no clean lint result is asserted.

The supplied lab ends at Task 4. Utilities, CLI, tests and documentation are reconstructed. Original core models and patterns are retained with small fixes for empty names, zero-price breakdown, bulk discounts and per-instance log files. The inventory is in memory; CSV is an export, not automatic persistence. Email notifications are simulated. Prices use floats for this educational example.
