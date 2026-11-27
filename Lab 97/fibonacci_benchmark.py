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

def fibonacci_recursive(n):
    """Recursive Fibonacci implementation (inefficient but CPU-intensive)"""
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

def fibonacci_iterative(n):
    """Iterative Fibonacci implementation"""
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def fibonacci_loop_intensive(n):
    """Loop-intensive Fibonacci calculation"""
    result = 0
    for i in range(n):
        if i <= 1:
            result += i
        else:
            # Simulate more complex calculation
            temp = 0
            for j in range(i):
                temp += j * 0.1
            result += int(temp) % 1000
    return result

def benchmark_function(func, n, description):
    """Benchmark a function and return execution time"""
    print(f"\nTesting {description} with n={n}")
    start_time = time.perf_counter()
    result = func(n)
    end_time = time.perf_counter()
    execution_time = end_time - start_time

    if isinstance(result, int) and result.bit_length() > 10000:
        print(f"Result size: {result.bit_length()} bits")
    else:
        print(f"Result: {result}")
    print(f"Execution Time: {execution_time:.4f} seconds")
    return execution_time

if __name__ == "__main__":
    if not verified_jit_build():
        sys.exit("Native JIT build not verified; comparison skipped.")
    if os.environ.get("PYTHON_JIT") not in ("0", "1"):
        sys.exit("Set PYTHON_JIT explicitly to 0 or 1.")
    jit_status = "ENABLED" if os.environ.get('PYTHON_JIT') == '1' else "DISABLED"
    print(f"Python JIT Compiler: {jit_status}")
    print(f"Python Version: {sys.version}")
    print("=" * 60)

    # Test parameters
    recursive_n = 35  # Keep this small for recursive version
    iterative_n = 100000
    loop_intensive_n = 2000

    # Benchmark different implementations
    times = {}

    # Recursive Fibonacci (small n due to exponential complexity)
    times['recursive'] = benchmark_function(
        fibonacci_recursive, recursive_n,
        f"Recursive Fibonacci (n={recursive_n})"
    )

    # Iterative Fibonacci
    times['iterative'] = benchmark_function(
        fibonacci_iterative, iterative_n,
        f"Iterative Fibonacci (n={iterative_n})"
    )

    # Loop-intensive calculation
    times['loop_intensive'] = benchmark_function(
        fibonacci_loop_intensive, loop_intensive_n,
        f"Loop-intensive calculation (n={loop_intensive_n})"
    )

    print("\n" + "=" * 60)
    print("SUMMARY OF EXECUTION TIMES:")
    for test_name, exec_time in times.items():
        print(f"{test_name.capitalize()}: {exec_time:.4f} seconds")
