# Interview Guide

These answers describe the initial implementation, not future roadmap items.

## Why did you analyze logs deterministically before calling AI?
Deterministic rules produce reproducible counts and evidence. AI can help interpret that evidence, but should not replace measurable checks or present an unverified hypothesis as fact.

## How do you group repeated errors?
The analysis engine normalizes selected variable values such as IP addresses, UUID-like values, and long numeric identifiers, then hashes the normalized message into a fingerprint. Normalization can still merge messages that differ in meaningful ways, so it is a heuristic.

## How is severity assigned?
The current rules give critical events critical severity, repeated errors higher severity than isolated errors, and repeated warnings medium severity. These defaults are not tied to business impact and must be configured for a real service.

## What does the error rate mean?
It is the number of ERROR and CRITICAL events divided by all parsed events, expressed as a percentage. It is not an HTTP request failure rate unless the input and counting policy specifically support that interpretation.

## What does an error-burst finding prove?
It shows that a configured number of timestamped error events fell within a five-minute bucket. It does not establish statistical significance, user impact, or the root cause.

## Why is AI optional?
The core application stays useful offline and avoids a mandatory paid dependency. A provider outage or invalid response should not prevent log analysis or report export.

## How do you reduce prompt injection risk?
The prompt tells the model to treat logs as untrusted evidence, the application does not execute model output, and requests are limited and redacted. These are layered safeguards, not a proof of complete immunity.

## How do you handle secret leakage?
The app uses basic pattern redaction and sensitive-key redaction before Bedrock requests. Regex redaction is best-effort and cannot guarantee that every credential or personal detail will be removed. Operators must review inputs before consent.

## Why is automatic remediation disabled?
A wrong restart or cloud mutation can worsen an outage. The initial system is an analysis and recommendation tool; any future action execution should require policy checks, permissions, approval, and verification.

## How would you productionize it?
Add authenticated access, durable storage, tenant isolation, stronger secret detection, audit logs, streaming ingestion, load testing, observability, tighter IAM policies, controlled deployment, and an independent security review.

## What is the current AWS deployment status?
The initial local version includes an optional Bedrock adapter. CloudWatch monitoring and an AWS deployment are not implemented by this milestone. Be precise about what has been tested in your own environment.
