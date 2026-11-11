"""Report local prerequisites without printing secrets or credential values."""

from __future__ import annotations

import importlib.util
import platform
import shutil
import sys


def main() -> int:
    print(f"Python: {platform.python_version()} ({sys.executable})")
    print(f"Platform: {platform.platform()}")
    for name in ("streamlit", "boto3", "dotenv", "pytest", "ruff"):
        print(f"Module {name}: {'available' if importlib.util.find_spec(name) else 'missing'}")
    for command in ("git", "docker"):
        print(f"Command {command}: {shutil.which(command) or 'not found'}")
    print("No credential values were inspected or printed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
