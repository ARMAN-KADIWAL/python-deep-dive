"""Syntax checks for all newly added labs, excluding no runnable Python files."""
from pathlib import Path
import py_compile
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
LABS = [64, 83, 84, 85, 86, 87, 88, 89, 90, 92, 98, 99, 100]


def run(lab, *args):
    subprocess.run([sys.executable, *args], cwd=ROOT / f"Lab {lab}", check=True, timeout=180)


def main():
    paths = [p for n in LABS for p in (ROOT / f"Lab {n}").rglob("*.py")]
    for p in paths:
        py_compile.compile(str(p), doraise=True)
    print(f"Syntax checks passed: {len(paths)} Python files")
    run(64, "final_project_analysis.py")
    for lab in (85, 86, 92, 98):
        for p in sorted((ROOT / f"Lab {lab}").glob("*.py")):
            run(lab, p.name)
    run(89, "basic_cli.py", "Hello")
    run(89, "help_demo.py", "--version")
    run(90, "good_style.py")
    run(90, "pep8_function.py")
    run(99, "main.py")
    run(99, "-m", "src.advanced_types")
    run(99, "-m", "unittest", "discover", "-s", "tests", "-v")
    run(100, "-m", "pytest", "tests", "-q")
    print("Selected functional checks passed; live HTTP and public deployment are not tested.")


if __name__ == "__main__":
    main()
