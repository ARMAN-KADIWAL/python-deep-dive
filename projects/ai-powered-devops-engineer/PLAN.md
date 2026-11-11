# Project Plan

## Problem
Application logs contain operational evidence, but repeated messages, spikes, and missing context make manual incident triage slow. This project groups evidence and optionally asks an AI model to suggest investigation paths.

## Target users
Students learning Python, AWS, DevOps, and evidence-driven incident triage.

## Version 1 scope
1. Parse local logs safely.
2. Normalize common fields into events.
3. Calculate severity counts, error rates, repeated fingerprints, and simple error bursts.
4. Create incident-style findings.
5. Export JSON and Markdown.
6. Keep AI optional and consent-gated.
7. Add tests and documentation.

## Out of scope
Automatic remediation, command execution, multi-user authentication, durable multi-tenant storage, Kubernetes management, and automatically creating AWS resources.

## Architecture choices
- Modular monolith keeps the system understandable and inexpensive.
- Deterministic analysis runs before optional AI, making findings reproducible and testable.
- AI is an optional adapter, so local analysis still works when a provider is down.
- In-memory state keeps the initial version simple but is not durable storage.
- Synthetic data supports repeatable demos without exposing private logs.
- Cloud integrations should be read-only by default.

## Security and privacy
Logs are untrusted input. Enforce file size limits, validate parsing, never execute log contents, and redact common secrets before optional AI requests. Remote requests require explicit operator action and consent. Use the standard AWS credential provider chain.

## Cost controls
Local use needs no AWS service. Bedrock may incur charges. No cloud resources are created by local setup. Before any cloud deployment, document resources, permissions, public exposure, cost drivers, and cleanup.

## Development sequence
1. Configuration and project structure
2. Log ingestion and normalization
3. Deterministic analysis
4. Reports and dashboard
5. Optional AI provider and safe fallback
6. Tests, security checks, container packaging, and CI
7. Optional monitoring integrations
8. Deployment documentation and verification

## Definition of done
A feature is complete only when its implementation, tests, docs, safe failure handling, and verification record exist. Creating a file alone is not proof of completion.
