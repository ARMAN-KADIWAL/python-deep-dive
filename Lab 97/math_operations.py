#!/usr/bin/env python3.13
import time
import sys

def simple_math_operations(n):
    """Perform simple mathematical operations in a loop"""
    result = 0
    for i in range(n):
        result += i * 2
        result -= i // 2
        result *= 1.1
        result /= 1.05
        result %= 1_000_000_000  # Keep the recurrence finite
    return result

def measure_execution_time(func, *args):
    """Measure the execution time of a function"""
    start_time = time.perf_counter()
    result = func(*args)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return result, execution_time

if __name__ == "__main__":
    # Test with different iteration counts
    test_sizes = [100000, 500000, 1000000]

    print("Python Version:", sys.version)
    print("Testing simple mathematical operations...")
    print("-" * 50)

    for size in test_sizes:
        result, exec_time = measure_execution_time(simple_math_operations, size)
        print(f"Iterations: {size:,}")
        print(f"Result: {result:.2f}")
        print(f"Execution Time: {exec_time:.4f} seconds")
        print("-" * 30)
