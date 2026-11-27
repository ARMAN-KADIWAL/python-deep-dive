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
from decimal import Decimal
import random

class DataTypeBenchmark:
    def __init__(self):
        self.jit_enabled = os.environ.get('PYTHON_JIT') == '1'

    def time_operation(self, func, *args, runs=3):
        """Time an operation multiple times"""
        times = []
        for _ in range(runs):
            start = time.perf_counter()
            result = func(*args)
            end = time.perf_counter()
            times.append(end - start)
        return min(times), result  # Return best time

    def test_integer_operations(self, n=1000000):
        """Test integer arithmetic operations"""
        def integer_ops():
            result = 0
            for i in range(n):
                result += i
                result *= 2
                result //= 3
                result -= i // 2
            return result

        return self.time_operation(integer_ops)

    def test_float_operations(self, n=1000000):
        """Test floating-point operations"""
        def float_ops():
            result = 0.0
            for i in range(n):
                result += float(i)
                result *= 2.5
                result /= 3.7
                result -= float(i) / 2.1
            return result

        return self.time_operation(float_ops)

    def test_complex_operations(self, n=100000):
        """Test complex number operations"""
        def complex_ops():
            result = complex(0, 0)
            for i in range(n):
                c = complex(i, i + 1)
                result += c
                result *= complex(1.1, 0.9)
                result /= complex(2.0, 1.5)
            return result

        return self.time_operation(complex_ops)

    def test_string_operations(self, n=10000):
        """Test string operations"""
        def string_ops():
            result = ""
            base_string = "Hello World "
            for i in range(n):
                result += base_string + str(i)
                if len(result) > 50000:  # Prevent excessive memory usage
                    result = result[-25000:]
            return len(result)

        return self.time_operation(string_ops)

    def test_list_operations(self, n=100000):
        """Test list operations"""
        def list_ops():
            data = []
            for i in range(n):
                data.append(i)
                if i % 100 == 0:
                    data.extend([i, i+1, i+2])
                if len(data) > 50000:
                    data = data[-25000:]
            return len(data)

        return self.time_operation(list_ops)

    def test_dict_operations(self, n=50000):
        """Test dictionary operations"""
        def dict_ops():
            data = {}
            for i in range(n):
                data[f"key_{i}"] = i * 2
                data[f"str_{i}"] = str(i)
                if i % 1000 == 0:
                    # Clean up to prevent excessive memory usage
                    if len(data) > 10000:
                        keys_to_remove = list(data.keys())[:5000]
                        for key in keys_to_remove:
                            del data[key]
            return len(data)

        return self.time_operation(dict_ops)

    def test_set_operations(self, n=100000):
        """Test set operations"""
        def set_ops():
            data = set()
            for i in range(n):
                data.add(i)
                data.add(str(i))
                if i % 2 == 0:
                    data.discard(i // 2)
            return len(data)

        return self.time_operation(set_ops)

    def run_all_tests(self):
        """Run all data type tests"""
        tests = {
            'Integer Operations': self.test_integer_operations,
            'Float Operations': self.test_float_operations,
            'Complex Operations': self.test_complex_operations,
            'String Operations': self.test_string_operations,
            'List Operations': self.test_list_operations,
            'Dictionary Operations': self.test_dict_operations,
            'Set Operations': self.test_set_operations
        }

        print(f"Data Type Performance Tests")
        print(f"JIT Compiler: {'ENABLED' if self.jit_enabled else 'DISABLED'}")
        print("=" * 60)

        results = {}
        for test_name, test_func in tests.items():
            print(f"\nTesting {test_name}...")
            try:
                exec_time, result = test_func()
                results[test_name] = {
                    'time': exec_time,
                    'result': str(result)[:50]  # Truncate long results
                }
                print(f"  Execution Time: {exec_time:.4f} seconds")
                print(f"  Result: {str(result)[:50]}")
            except Exception as e:
                print(f"  Error: {e}")
                results[test_name] = {'error': str(e)}

        return results

if __name__ == "__main__":
    if not verified_jit_build():
        sys.exit("Native JIT build not verified; comparison skipped.")
    if os.environ.get("PYTHON_JIT") not in ("0", "1"):
        sys.exit("Set PYTHON_JIT explicitly to 0 or 1.")
    benchmark = DataTypeBenchmark()
    results = benchmark.run_all_tests()

    # Save results
    jit_suffix = "with_jit" if benchmark.jit_enabled else "without_jit"
    filename = f"datatype_results_{jit_suffix}.txt"

    with open(filename, 'w') as f:
        f.write(f"Data Type Performance Results\n")
        f.write(f"JIT: {'ENABLED' if benchmark.jit_enabled else 'DISABLED'}\n")
        f.write("=" * 50 + "\n")

        for test_name, result in results.items():
            f.write(f"\n{test_name}:\n")
            if 'error' in result:
                f.write(f"  Error: {result['error']}\n")
            else:
                f.write(f"  Time: {result['time']:.4f} seconds\n")
                f.write(f"  Result: {result['result']}\n")

    print(f"\nResults saved to {filename}")
