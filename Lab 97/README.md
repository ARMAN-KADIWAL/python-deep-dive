# Lab 97 — Experimental JIT Compiler

Six benchmark and reporting modules from the supplied lab. The missing analysis report is reconstructed. Python 3.13 must be compiled with native experimental JIT support. This package conservatively checks explicit build flags in CONFIG_ARGS; flags confirm build configuration, not that a specific function executed as native code. Unknown build configurations are rejected rather than assumed supported.

Run on a suitable CPython build:
```bash
python3.13 -c 'import sysconfig; print(sysconfig.get_config_var("CONFIG_ARGS"))'
PYTHON_JIT=0 python3.13 math_operations.py
PYTHON_JIT=1 python3.13 math_operations.py
for mode in 0 1; do
  PYTHON_JIT=$mode python3.13 fibonacci_benchmark.py
  PYTHON_JIT=$mode python3.13 comprehensive_benchmark.py
  PYTHON_JIT=$mode python3.13 datatype_benchmark.py
done
python3.13 compare_results.py
python3.13 jit_analysis.py
```

Corrections: explicit requested JIT settings, native-build checks, warm-up, finite arithmetic recurrence, smaller Fibonacci workload and safe result size output. Five-percent bands are descriptive thresholds, not statistical significance. Compare identical workloads on the same runtime and host. No real JIT speedups are asserted in the absence of measurements. Python 3.12 can run math operations as a baseline, but cannot complete this native CPython JIT comparison.

Reference: https://docs.python.org/3.13/using/configure.html
