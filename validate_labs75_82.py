import argparse
import ast
import hashlib
import importlib.metadata
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SMOKE = {
    75: [(name,) for name in (
        "basic_threading.py", "sequential_vs_concurrent.py", "gil_demonstration.py",
        "performance_measurement.py", "advanced_threading.py", "thread_lifecycle.py",
        "race_condition_demo.py", "thread_synchronization.py", "advanced_locks.py",
        "thread_monitoring.py",
    )],
    76: [(name,) for name in (
        "counter_without_lock.py", "counter_with_lock.py", "lock_comparison.py",
        "deadlock_demo.py", "deadlock_prevention.py", "producer_consumer.py",
    )],
    77: [(name,) for name in (
        "basic_multiprocessing.py", "performance_comparison.py", "process_pool_demo.py",
        "queue_communication.py", "parallel_factorial.py", "advanced_multiprocessing.py",
    )],
    78: [("sync_example.py",), ("async_example.py",), ("coroutines_demo.py",),
         ("async_error_handling.py",), ("gather_demo.py", "--offline"),
         ("concurrency_patterns.py",), ("event_loop_demo.py",),
         ("event_loop_debug.py",), ("performance_comparison.py",)],
    79: [("main.py", "--offline"), ("enhanced_scraper.py", "--offline")],
    80: [("basic_socket.py",), ("socket_comparison.py",)],
    81: [],
    82: [],
}


def run(command, folder, log_path):
    started = time.perf_counter()
    completed = subprocess.run(
        [sys.executable, *command], cwd=folder,
        capture_output=True, text=True, timeout=120,
    )
    output = completed.stdout + "\n" + completed.stderr
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(output, encoding="utf-8")
    result = {
        "command": ["python", *command], "exit_code": completed.returncode,
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "log": str(log_path.relative_to(ROOT)),
    }
    if completed.returncode != 0:
        raise RuntimeError(f"Command failed: {command}\n{output[-10000:]}")
    if "was never awaited" in completed.stderr or "leaked shared_memory" in completed.stderr:
        raise RuntimeError(f"Resource/coroutine warning: {command}\n{completed.stderr}")
    return result, output


def validate(include_smoke=False):
    dependencies = {}
    for name in ("aiohttp", "beautifulsoup4", "numpy", "requests"):
        dependencies[name] = importlib.metadata.version(name)
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version.split()[0], "dependencies": dependencies,
        "network_scope": "Controlled loopback HTTP/TCP/UDP; public httpbin.org was not used.",
        "smoke_enabled": include_smoke, "labs": [], "source_sha256": {},
    }
    output_root = ROOT / "validation-output"
    for lab in range(75, 83):
        folder = ROOT / f"Lab {lab}"
        sources = sorted(folder.glob("*.py"))
        for path in sources:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            report["source_sha256"][str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
        unit, output = run(
            ["-m", "unittest", "discover", "-v", "-p", f"test_lab{lab}.py"],
            folder, output_root / f"Lab {lab}" / "unittest.log",
        )
        match = re.search(r"Ran (\d+) tests?", output)
        if match is None or int(match.group(1)) == 0:
            raise RuntimeError(f"No tests executed for Lab {lab}")
        item = {"lab": lab, "python_files": len(sources), "unit_tests": int(match.group(1)),
                "unit": unit, "smoke": [], "passed": True}
        print(f"PASS Lab {lab}: {item['unit_tests']} tests; {len(sources)} Python files compile", flush=True)
        if include_smoke:
            for command in SMOKE[lab]:
                result, output = run(list(command), folder, output_root / f"Lab {lab}" / (Path(command[0]).stem + ".log"))
                item["smoke"].append(result)
                print(f"PASS Lab {lab} {command[0]}: {result['elapsed_seconds']:.2f}s", flush=True)
        report["labs"].append(item)
    report["total_unit_tests"] = sum(item["unit_tests"] for item in report["labs"])
    report["smoke_runs"] = sum(len(item["smoke"]) for item in report["labs"])
    report["all_passed"] = True
    report["limits"] = [
        "Benchmarks are illustrative single runs, not universal speed guarantees.",
        "Intentional race/deadlock and handled-error demos are labelled in their output.",
        "Persistent servers and interactive clients are exercised by owned-server integration tests.",
        "Local network checks do not validate an external cloud firewall or public website availability.",
    ]
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--report", default="validation-output/labs75-82-verification.json")
    args = parser.parse_args()
    report = validate(args.smoke)
    destination = ROOT / args.report
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"PASS: {report['total_unit_tests']} unit/integration tests; {report['smoke_runs']} smoke runs.")
    print(f"Report: {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
