# Lab 71 — Debugging Techniques and Tools

The full lesson is in [LAB_GUIDE.md](LAB_GUIDE.md).

## Linux quick start

```bash
cd 'Lab 71'
python3 fixed_calculator.py
python3 -m unittest discover -v -p 'test_*.py'
```

The `intentional_bugs/` folder contains **deliberately broken** practice
scripts. They are provided to reproduce errors; they are not final solutions.
Do **not** execute them expecting a clean run. `pdb_example.py` and some other
demonstrations can start the interactive debugger and require terminal input.

`fixed_calculator.py` is the corrected calculator; its assertions are checked
by `test_fixed_calculator.py`.

Use `python3 -m pdb file.py` for a Python debugger session; type `help` for
commands, `n` for next line, `s` to enter a function, `c` to continue and `q`
to quit.
