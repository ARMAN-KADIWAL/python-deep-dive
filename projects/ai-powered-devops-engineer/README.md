# AI-Powered DevOps Engineer

A local-first, evidence-driven tool for application log analysis, incident triage, and optional AI-assisted diagnosis. This is a practical Cloud + AI engineering portfolio project.

## Initial features

- Upload supported plain-text or JSON Lines logs.
- Parse timestamps, levels, service names, and HTTP status codes when present.
- Group repeated errors using normalized fingerprints.
- Calculate event counts and error rates.
- Detect configurable error bursts.
- Inspect findings and supporting evidence.
- Export JSON and Markdown reports.
- Run core analysis without AWS credentials or a paid AI API.
- Optionally use Amazon Bedrock only after configuration and explicit user consent.

## Requirements

Python 3.11 or later and pip. Docker is optional. AWS credentials and Bedrock access are not required for local log analysis. The Docker SDK is an optional monitoring extra.

## Local setup

Windows PowerShell:

    py -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -e ".[dev,monitoring]"
    streamlit run app.py

Linux or macOS:

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install -e ".[dev,monitoring]"
    streamlit run app.py

Open the local URL printed by Streamlit, usually http://localhost:8501.

## Using the application

1. Select a synthetic sample incident or upload a log file.
2. Run analysis.
3. Review parsing results, metrics, findings, and evidence.
4. Download a JSON or Markdown report.
5. Choose AWS CloudWatch Logs to explicitly approve a bounded, read-only query against an existing log group. This needs an AWS profile or IAM role with narrowly scoped `logs:FilterLogEvents` permission.
6. Open the optional Docker status section and approve inspection before querying an already-running local Docker daemon. Docker socket access is privileged; no socket is mounted by the supplied Compose file.
7. For optional Bedrock diagnosis, configure the Region and model ID, enable the integration, and explicitly approve sending sanitized evidence to the selected AWS model.

Sample data is synthetic. Do not upload confidential production logs unless you have approval and understand data-handling implications.

## Supported input

Plain-text logs, JSON Lines, recognizable HTTP access lines, and unstructured non-empty lines are supported. Unclassified lines are retained as UNKNOWN events. Timestamps without timezone information are treated as UTC. Malformed JSON records are counted as rejected lines.

## Security boundaries

- Logs are untrusted data and are never executed.
- AI is optional and must be enabled by the operator.
- A confirmation is required before sending sanitized evidence to AWS.
- The app does not perform automatic remediation.
- No cloud infrastructure is created by the local application.
- Never commit real logs, credentials, or sensitive reports.

See docs/architecture.md, docs/threat-model.md, and docs/deployment.md.

## Current limitations

- Incidents are not persisted across app restarts.
- Error-spike detection is a configurable rule, not a statistically calibrated model.
- Bedrock diagnoses are hypotheses and require human verification.
- Docker status inspection and CloudWatch Logs read-only adapters have CI unit tests using mocked integrations, but have not been tested against a real Docker daemon or AWS account. Docker inspection requires the optional SDK extra. The Docker socket is not mounted into the Compose container.
- Production use would require authentication, durable storage, load testing, security review, and operational monitoring.

## Roadmap

- [x] Local log parsing and deterministic analysis
- [x] Evidence-backed findings and report export
- [x] Optional consent-gated Bedrock adapter
- [-] Read-only Docker status and CloudWatch Logs adapter/UI, verification pending
- [x] CI checks: tests, lint, formatting, Bandit, dependency audit, app startup, Docker build, and container smoke test
- [ ] Deployment review and real screenshots

## Tests

    pytest
    ruff check .
    ruff format --check .
    bandit -r src app.py

GitHub Actions currently verifies 26 passing tests at 84% total measured coverage, Ruff lint/formatting, Bandit, pip-audit, Streamlit startup, Docker image build, and container health startup. Check the linked Actions run for the latest commit. Live Bedrock, CloudWatch, and local Docker-daemon integrations still require testing in a configured environment.

## License

MIT. See LICENSE.
