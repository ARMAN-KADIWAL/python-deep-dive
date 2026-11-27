#!/usr/bin/env python3.13
import json
import os
import sys
from datetime import datetime

class JITAnalysis:
    def __init__(self):
        self.analysis_results = {}

    def load_benchmark_data(self):
        """Load all benchmark data files"""
        data = {}
        files_to_load = [
            'benchmark_results_without_jit.json',
            'benchmark_results_with_jit.json'
        ]

        for filename in files_to_load:
            if os.path.exists(filename):
                try:
                    with open(filename, 'r') as f:
                        data[filename] = json.load(f)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")

        return data

    def analyze_performance_patterns(self, data):
        """Analyze performance patterns across different test types"""
        if len(data) < 2:
            return "Insufficient data for analysis"

        without_jit = None
        with_jit = None

        for filename, content in data.items():
            if 'without_jit' in filename:
                without_jit = content
            elif 'with_jit' in filename:
                with_jit = content

        if not without_jit or not with_jit:
            return "Missing JIT comparison data"

        analysis = {
            'improvements': [],
            'degradations': [],
            'no_change': [],
            'patterns': {}
        }

        for test_name in without_jit.get('results', {}):
            if test_name in with_jit.get('results', {}):
                without_time = without_jit['results'][test_name].get('mean', 0)
                with_time = with_jit['results'][test_name].get('mean', 0)

                if without_time > 0 and with_time > 0:
                    improvement = ((without_time - with_time) / without_time) * 100

                    if improvement > 5:  # Significant improvement
                        analysis['improvements'].append({
                            'test': test_name,
                            'improvement': improvement,
                            'speedup': without_time / with_time
                        })
                    elif improvement < -5:  # Significant degradation
                        analysis['degradations'].append({
                            'test': test_name,
                            'degradation': abs(improvement),
                            'slowdown': with_time / without_time
                        })
                    else:
                        analysis['no_change'].append(test_name)

        return analysis

    def identify_jit_advantages(self, analysis):
        """Identify advantages of JIT compilation"""
        advantages = []

        if analysis['improvements']:
            advantages.append("Performance Improvements Observed:")
            for item in analysis['improvements']:
                advantages.append(f"  - {item['test']}: {item['improvement']:.1f}% faster ({item['speedup']:.2f}x speedup)")

        # Analyze patterns
        if len(analysis['improvements']) > len(analysis['degradations']):
            advantages.append("\nOverall Positive Impact:")
            advantages.append("  - JIT shows more improvements than degradations")

        # Specific advantages based on test types
        improvement_tests = [item['test'] for item in analysis['improvements']]

        if any('arithmetic' in test for test in improvement_tests):
            advantages.append("\nArithmetic Operations:")
            advantages.append("  - JIT optimizes mathematical computations effectively")

        if any('loop' in test for test in improvement_tests):
            advantages.append("\nLoop Optimization:")
            advantages.append("  - JIT can optimize repetitive loop structures")

        if any('function' in test for test in improvement_tests):
            advantages.append("\nFunction Call Optimization:")
            advantages.append("  - JIT reduces function call overhead")

        return advantages

    def identify_jit_limitations(self, analysis):
        """Identify limitations of JIT compilation"""
        limitations = []

        if analysis['degradations']:
            limitations.append("Performance Degradations Observed:")
            for item in analysis['degradations']:
                limitations.append(f"  - {item['test']}: {item['degradation']:.1f}% slower ({item['slowdown']:.2f}x slowdown)")

        # General limitations
        limitations.extend([
            "\nGeneral JIT Limitations:",
            "  - Compilation overhead for short-running programs",
            "  - Memory overhead for storing compiled code",
            "  - Experimental status in Python 3.13",
            "  - May not optimize all Python constructs effectively",
            "  - Warm-up time required for optimization to take effect"
        ])

        # Specific limitations based on test results
        degradation_tests = [item['test'] for item in analysis['degradations']]

        if any('string' in test for test in degradation_tests):
            limitations.append("\nString Operations:")
            limitations.append("  - JIT may not optimize string manipulations effectively")

        if any('list' in test or 'dict' in test for test in degradation_tests):
            limitations.append("\nData Structure Operations:")
            limitations.append("  - Complex data structure operations may not benefit from JIT")

        return limitations

    def generate_report(self):
        """Generate a comprehensive JIT analysis report."""
        data = self.load_benchmark_data()
        without = data.get("benchmark_results_without_jit.json", {})
        with_jit = data.get("benchmark_results_with_jit.json", {})
        if not (
            without.get("jit_build_verified") is True
            and with_jit.get("jit_build_verified") is True
            and without.get("jit_enabled") is False
            and with_jit.get("jit_enabled") is True
            and without.get("python_version") == with_jit.get("python_version")
        ):
            print("Comparison unavailable: verify native JIT build and matched runs.")
            return
        analysis = self.analyze_performance_patterns(data)

        if not isinstance(analysis, dict):
            print(analysis)
            return

        self.analysis_results = analysis
        advantages = self.identify_jit_advantages(analysis)
        limitations = self.identify_jit_limitations(analysis)

        report = [
            "JIT COMPILER PERFORMANCE ANALYSIS",
            "=" * 70,
            f"Generated: {datetime.now().isoformat()}",
            f"Benchmark Python Version: {without['python_version']}",
            "",
            "Note: JIT mode labels represent requested settings.",
            "Build flags are checked; native compilation of each function is not proven.",
            "",
            "PERFORMANCE SUMMARY",
            "-" * 70,
            f"Improvements: {len(analysis['improvements'])}",
            f"Degradations: {len(analysis['degradations'])}",
            f"No significant change: {len(analysis['no_change'])}",
            "",
            "ADVANTAGES",
            "-" * 70
        ]
        report.extend(advantages or ["No significant improvements observed."])
        report.extend(["", "LIMITATIONS", "-" * 70])
        report.extend(limitations)
        report.extend([
            "",
            "RECOMMENDED USE CASES",
            "-" * 70,
            "1. CPU-intensive mathematical calculations",
            "2. Repetitive loops",
            "3. Long-running computational workloads",
            "",
            "CONCLUSION",
            "-" * 70,
            "JIT performance depends on workload and runtime.",
            "Benchmark results must be interpreted carefully.",
            "JIT does not guarantee faster execution.",
            "=" * 70
        ])

        report_text = "\n".join(report)
        print(report_text)
        with open("jit_analysis_report.txt", "w", encoding="utf-8") as file:
            file.write(report_text)
        with open("jit_analysis_results.json", "w", encoding="utf-8") as file:
            json.dump(analysis, file, indent=4)
        print("\nAnalysis report saved successfully!")


if __name__ == "__main__":
    analyzer = JITAnalysis()
    analyzer.generate_report()
