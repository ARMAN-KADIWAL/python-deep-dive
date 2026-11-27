#!/usr/bin/env python3.13
import time
import sys
import sysconfig
import shlex


def verified_jit_build():
    """Check explicit configure flags; unknown builds are not assumed enabled."""
    if sys.version_info < (3, 13):
        return False
    flags = shlex.split(sysconfig.get_config_var("CONFIG_ARGS") or "")
    return any(flag in (
        "--enable-experimental-jit",
        "--enable-experimental-jit=yes",
        "--enable-experimental-jit=yes-off",
    ) for flag in flags)


import os
import statistics
import json
from datetime import datetime

class JITBenchmark:
    def __init__(self):
        self.results = {}
        self.jit_enabled = os.environ.get('PYTHON_JIT') == '1'

    def time_function(self, func, *args, runs=5):
        """Time a function multiple times and return statistics"""
        func(*args)  # Warm-up before measured runs
        times = []
        for _ in range(runs):
            start = time.perf_counter()
            result = func(*args)
            end = time.perf_counter()
            times.append(end - start)

        return {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'min': min(times),
            'max': max(times),
            'std_dev': statistics.stdev(times) if len(times) > 1 else 0,
            'result': result
        }

    def benchmark_arithmetic_operations(self):
        """Benchmark basic arithmetic operations"""
        def arithmetic_intensive(n):
            result = 0.0
            for i in range(n):
                result += i * 3.14159
                result -= i / 2.71828
                result *= 1.41421
                result /= 1.73205
            return result

        return self.time_function(arithmetic_intensive, 1000000)

    def benchmark_list_operations(self):
        """Benchmark list operations"""
        def list_operations(n):
            data = list(range(n))
            result = []
            for i in data:
                result.append(i ** 2)
                if i % 2 == 0:
                    result.append(i // 2)
            return len(result)

        return self.time_function(list_operations, 50000)

    def benchmark_string_operations(self):
        """Benchmark string operations"""
        def string_operations(n):
            text = "Hello World! " * 100
            result = ""
            for i in range(n):
                result += text.upper().lower().replace("World", "Python")
                if len(result) > 10000:
                    result = result[:5000]  # Prevent excessive memory usage
            return len(result)

        return self.time_function(string_operations, 1000)

    def benchmark_nested_loops(self):
        """Benchmark nested loop operations"""
        def nested_loops(n):
            result = 0
            for i in range(n):
                for j in range(n):
                    result += i * j
                    if result > 1000000:
                        result = result % 1000000
            return result

        return self.time_function(nested_loops, 500)

    def benchmark_function_calls(self):
        """Benchmark function call overhead"""
        def helper_function(x, y):
            return x * y + x / (y + 1)

        def function_calls(n):
            result = 0
            for i in range(n):
                result += helper_function(i, i + 1)
            return result

        return self.time_function(function_calls, 100000)

    def run_all_benchmarks(self):
        """Run all benchmark tests"""
        benchmarks = {
            'arithmetic_operations': self.benchmark_arithmetic_operations,
            'list_operations': self.benchmark_list_operations,
            'string_operations': self.benchmark_string_operations,
            'nested_loops': self.benchmark_nested_loops,
            'function_calls': self.benchmark_function_calls
        }

        print(f"JIT Compiler: {'ENABLED' if self.jit_enabled else 'DISABLED'}")
        print(f"Python Version: {sys.version}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 70)

        for name, benchmark_func in benchmarks.items():
            print(f"\nRunning {name.replace('_', ' ').title()}...")
            try:
                result = benchmark_func()
                self.results[name] = result
                print(f"  Mean Time: {result['mean']:.4f} seconds")
                print(f"  Median Time: {result['median']:.4f} seconds")
                print(f"  Min Time: {result['min']:.4f} seconds")
                print(f"  Max Time: {result['max']:.4f} seconds")
                print(f"  Std Dev: {result['std_dev']:.4f} seconds")
            except Exception as e:
                print(f"  Error: {e}")
                self.results[name] = {'error': str(e)}

        return self.results

    def save_results(self, filename):
        """Save results to JSON file"""
        data = {
            'jit_enabled': self.jit_enabled,
            'jit_build_verified': verified_jit_build(),
            'python_version': sys.version,
            'timestamp': datetime.now().isoformat(),
            'results': self.results
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\nResults saved to {filename}")

if __name__ == "__main__":
    if not verified_jit_build():
        sys.exit("Native JIT build not verified; comparison skipped.")
    if os.environ.get("PYTHON_JIT") not in ("0", "1"):
        sys.exit("Set PYTHON_JIT explicitly to 0 or 1.")
    benchmark = JITBenchmark()
    results = benchmark.run_all_benchmarks()

    # Save results with appropriate filename
    jit_suffix = "with_jit" if benchmark.jit_enabled else "without_jit"
    filename = f"benchmark_results_{jit_suffix}.json"
    benchmark.save_results(filename)
