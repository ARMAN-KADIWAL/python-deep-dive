# Testing and Validation

Run commands from the AI-Powered DevOps Engineer project directory.

## Install development tools

    python -m pip install -e ".[dev]"

## Automated tests

    pytest
    pytest --cov=devops_ai --cov-report=term-missing

Tests cover plain-text and JSONL parsing, timestamp normalization, upload size limits, repeated-error grouping, error burst thresholds, report serialization, configuration defaults, diagnosis validation, and secret redaction.

Unit tests must not contact AWS or a paid AI service. The Bedrock adapter requires a configured account and should be verified separately in an explicitly approved environment.

## Static checks

    ruff check .
    ruff format --check .
    bandit -r src app.py
    pip-audit

These commands have not yet been executed through the linked GitHub session. Run them before describing the code as verified.

## Docker

    docker compose config
    docker compose build
    docker compose up

The service binds to localhost port 8501 by default. Stop with Ctrl+C or docker compose down.

## Manual acceptance checklist

- Load each synthetic sample.
- Confirm event counts match the fixture.
- Confirm repeated database errors group together.
- Confirm error burst finding appears when the threshold is met.
- Download JSON and Markdown reports.
- Confirm offline diagnosis labels itself as a demo.
- Confirm no AWS call occurs without configuration and explicit consent.
- Try an oversized upload and malformed JSONL.
- Confirm unavailable AI does not erase the deterministic report.

Record actual results and the environment used before release.
