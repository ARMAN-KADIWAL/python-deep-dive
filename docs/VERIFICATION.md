# Verification and scope

Repository coverage and execution evidence are distinct.

## Inventory

All 94 required folders from Labs 6–100 are present, excluding Lab 30. Source files and historical evidence remain in their original lab folders to preserve existing links.

## Recorded automated checks

### Labs 64, 83–90, 92, 98–100

- Run: [GitHub Actions #46041721824](https://github.com/ARMAN-KADIWAL/python-deep-dive/actions/runs/46041721824)
- Commit: [b0d2d11](https://github.com/ARMAN-KADIWAL/python-deep-dive/commit/b0d2d118a0bfad9853d772ccd468c80af0b781f6)
- Runner: Python 3.12.16 on Linux
- Result: success, 27 November 2026
- Syntax: 88 Python files.
- Selected functional checks passed, including offline HTTP fixtures, loopback REST CRUD, data analysis, regex, logging, CLI, refactoring and the typed project.
- Lab 98: mypy found no issues in 7 source files.
- Lab 99: mypy found no issues in 7 source files; 6 unit tests completed successfully.
- Lab 100: 11 tests passed, 5 warnings; exact line coverage 97.58% (124 statements, 3 missed). The workflow enforced at least 81%.

These results belong to the linked commit, not every lab or environment.

### Labs 75–82

The [original JSON report](verification/labs75-82-verification.json) preserves commands, outcomes, source hashes, timings and log paths. Raw logs remain in the original numbered lab folders.

### Other evidence

- [Lab 42](../Lab%2042/PROOF.md), [Lab 43](../Lab%2043/PROOF.md), [Lab 44](../Lab%2044/PROOF.md), [Lab 45](../Lab%2045/PROOF.md), [Lab 46](../Lab%2046/PROOF.md).
- [Lab 56 proof](../Lab%2056/proof/).
- [Lab 63 visualizations](../Lab%2063/proof/).

## Limits

No full-curriculum execution guarantee is claimed. Lab 97 native JIT verification requires a suitable interpreter. Public HTTP access, production cloud deployment, load testing and comprehensive security auditing are not established by these checks. Reconstructed handout endings are documented in individual labs. Intentional negative examples are retained.
