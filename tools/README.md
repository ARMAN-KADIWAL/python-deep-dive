# Validation tools

Run commands from the repository root in an environment where dependency installation is permitted.

## Labs 75–82

```bash
python -m pip install -r tools/requirements-labs75-82.txt
python tools/validate_labs75_82.py --smoke
```

Fresh results go to ignored `validation-output/`. The [historical report](../docs/verification/labs75-82-verification.json) references committed lab logs.

## Selected later labs (64, 83–90, 92, 98–100)

```bash
python -m pip install -r "Lab 64/requirements.txt" -r "Lab 83/requirements.txt" -r "Lab 98/requirements.txt" -r "Lab 100/requirements.txt" "pytest-cov>=6,<7"
MPLBACKEND=Agg python tools/validate_labs64-100.py
(cd "Lab 98" && python -m mypy *.py)
(cd "Lab 99" && python -m mypy src/ main.py tests/)
(cd "Lab 100" && python -m pytest tests/ -q --cov=src --cov-report=term-missing --cov-fail-under=81)
```

These commands use Bash syntax. GitHub Actions runs the checks when relevant files change. See [verification scope](../docs/VERIFICATION.md) for recorded results and limitations.
