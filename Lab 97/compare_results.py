#!/usr/bin/env python3.13
import json
import sys

def load_results(filename):
    """Load benchmark results from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filename}")
        return None

def compare_results(results_without_jit, results_with_jit):
    """Compare benchmark results and calculate performance improvements"""
    print("PERFORMANCE COMPARISON REPORT")
    print("=" * 70)

    if not results_without_jit or not results_with_jit:
        print("Error: Could not load one or both result files")
        return

    print(f"Without JIT - Python: {results_without_jit.get('python_version', 'Unknown')}")
    print(f"With JIT - Python: {results_with_jit.get('python_version', 'Unknown')}")
    print()

    # Compare each benchmark
    for test_name in results_without_jit.get('results', {}):
        if test_name in results_with_jit.get('results', {}):
            without_jit = results_without_jit['results'][test_name]
            with_jit = results_with_jit['results'][test_name]

            if 'error' in without_jit or 'error' in with_jit:
                print(f"{test_name.replace('_', ' ').title()}: Error in execution")
                continue

            without_time = without_jit.get('mean', 0)
            with_time = with_jit.get('mean', 0)

            if without_time > 0 and with_time > 0:
                improvement = ((without_time - with_time) / without_time) * 100
                speedup = without_time / with_time

                print(f"{test_name.replace('_', ' ').title()}:")
                print(f"  Without JIT: {without_time:.4f} seconds")
                print(f"  With JIT:    {with_time:.4f} seconds")
                print(f"  Improvement: {improvement:+.2f}%")
                print(f"  Speedup:     {speedup:.2f}x")

                if improvement > 0:
                    print(f"  Status:      JIT FASTER")
                elif improvement < 0:
                    print(f"  Status:      JIT SLOWER")
                else:
                    print(f"  Status:      NO DIFFERENCE")
                print()

def generate_summary(results_without_jit, results_with_jit):
    """Generate a summary of overall performance impact"""
    if not results_without_jit or not results_with_jit:
        return

    improvements = []

    for test_name in results_without_jit.get('results', {}):
        if test_name in results_with_jit.get('results', {}):
            without_jit = results_without_jit['results'][test_name]
            with_jit = results_with_jit['results'][test_name]

            if 'error' not in without_jit and 'error' not in with_jit:
                without_time = without_jit.get('mean', 0)
                with_time = with_jit.get('mean', 0)

                if without_time > 0 and with_time > 0:
                    improvement = ((without_time - with_time) / without_time) * 100
                    improvements.append(improvement)

    if improvements:
        avg_improvement = sum(improvements) / len(improvements)
        positive_improvements = [i for i in improvements if i > 0]
        negative_improvements = [i for i in improvements if i < 0]

        print("SUMMARY")
        print("=" * 70)
        print(f"Average Performance Change: {avg_improvement:+.2f}%")
        print(f"Tests with Improvement: {len(positive_improvements)}/{len(improvements)}")
        print(f"Tests with Degradation: {len(negative_improvements)}/{len(improvements)}")

        if positive_improvements:
            print(f"Best Improvement: {max(positive_improvements):.2f}%")
        if negative_improvements:
            print(f"Worst Degradation: {min(negative_improvements):.2f}%")

if __name__ == "__main__":
    # Load results
    results_without = load_results("benchmark_results_without_jit.json")
    results_with = load_results("benchmark_results_with_jit.json")

    if not results_without or not results_with:
        sys.exit("Missing comparison data.")
    if not (results_without.get("jit_build_verified") is True and results_with.get("jit_build_verified") is True and results_without.get("jit_enabled") is False and results_with.get("jit_enabled") is True and results_without.get("python_version") == results_with.get("python_version")):
        sys.exit("Comparison requires verified native JIT builds and matching Python versions with opposite requested settings.")
    # Compare and display results
    compare_results(results_without, results_with)
    generate_summary(results_without, results_with)
