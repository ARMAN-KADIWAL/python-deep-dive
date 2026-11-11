# Implementation Checklist

Status: [ ] not implemented, [-] implemented but environment verification pending, [x] implemented and CI-verified, [!] blocked.

## Foundation
- [x] Create project folder and architecture documentation.
- [x] Define local-first and no-automatic-remediation boundaries.
- [x] Define Python package, dependencies, settings, and ignore rules.
- [x] Verify application startup using the CI Streamlit health smoke test.
- [-] Run the app on the learner's own Windows machine.

## Core functionality
- [x] Parse plain-text logs and JSON Lines.
- [x] Normalize timestamps and classify common log levels.
- [x] Calculate event metrics and repeated-error findings.
- [x] Detect configurable error-count bursts.
- [x] Export JSON and Markdown reports.
- [x] Add unit tests for parsing, metrics, findings, reports, and configuration.
- [x] CI test suite: 26 tests passed.
- [x] CI branch coverage report: 84% total coverage.
- [x] Ruff lint and formatting checks pass.

## Dashboard and AI
- [x] Build Streamlit workflow for sample data and uploads.
- [x] Add explicitly labeled offline demo diagnosis provider.
- [x] Add optional Bedrock adapter with explicit consent.
- [x] Add structured response validation and basic secret redaction.
- [x] Unit-test Bedrock adapter with a mocked client; no real AWS call was made.
- [-] Validate model access, permissions, and costs in a configured AWS account.
- [-] Test provider behavior under a real network timeout or service outage.

## Monitoring integrations
- [x] Add read-only CloudWatch Logs reader with bounded event count and pagination.
- [x] Add CloudWatch unit tests using a mocked client.
- [-] Validate CloudWatch against an existing log group in an authorized AWS account.
- [x] Add read-only Docker status reader with bounded container listing.
- [x] Add Docker unit tests with a mocked daemon.
- [-] Validate Docker status against the learner's own Docker daemon.

## Security and packaging
- [x] Add upload size limit and safe parsing checks.
- [x] Add .env.example and ignore rules for real .env files.
- [x] Ruff lint and formatting checks pass in GitHub Actions.
- [x] Bandit Python security scan reports no issues.
- [x] pip-audit dependency audit passes after upgrading the vulnerable pytest constraint.
- [x] Docker image builds in GitHub Actions.
- [x] Docker container starts and its health endpoint passes in GitHub Actions.
- [x] Streamlit app starts and its health endpoint passes in GitHub Actions.
- [ ] Independent production security review and load test.

## AWS and deployment
- [x] Document CloudWatch read-only IAM policy template and setup.
- [x] Document cost, credentials, and data-handling boundaries.
- [ ] Deploy to AWS. No AWS resources have been created.
- [ ] Review current cost for the chosen deployment before provisioning.

## Portfolio
- [x] Add README, plan, architecture, threat model, testing guide, demo script, and interview guide.
- [x] Add a GitHub Actions CI workflow.
- [ ] Capture genuine dashboard screenshots after running it locally.
- [x] Prepare resume bullets based on implemented features; quantify no unmeasured improvements.
- [-] Review the draft pull request and keep it unmerged until personally reviewed.

## Latest verified checkpoint
- GitHub Actions run: 38700991788
- Unit tests: 26 passed
- Total measured coverage: 84%
- Ruff lint: pass
- Ruff format check: pass
- Bandit: no issues identified
- pip-audit: pass
- Streamlit health smoke test: pass
- Docker image build: pass
- Docker container health smoke test: pass
- Real AWS Bedrock and CloudWatch calls have not been tested.
- Live Docker inspection on the learner's machine has not been tested.
- No AWS resources were created and the default branch was not modified.
