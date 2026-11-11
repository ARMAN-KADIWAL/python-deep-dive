# Threat Model

## Assets

- Uploaded log content
- Derived findings and reports
- AWS credential-provider access
- Optional Bedrock request data
- Application configuration

## Trust boundaries

1. Uploaded files enter from an untrusted operator-selected source.
2. Parsed log text remains untrusted, including text that resembles instructions.
3. Optional AI requests cross a machine-to-AWS boundary.
4. AWS credentials are obtained through the configured AWS SDK provider chain and must never be shown in the UI.

## Threats and mitigations

### Malicious or oversized log files
Mitigation: enforce a configurable byte limit, decode UTF-8 safely, bound message length, and treat parser failures as data errors. The initial parser still loads the accepted file into memory, so large-scale ingestion needs a streaming implementation.

### Prompt injection inside logs
Mitigation: system instructions say log text is evidence, not instructions. The application does not execute model output. This is defense-in-depth, not a guarantee that a model cannot be manipulated.

### Secret leakage to an external provider
Mitigation: Bedrock calls require both configuration and explicit UI consent. The request is truncated and common secret patterns are redacted. Redaction is best-effort and can miss sensitive values; inspect input before approving any remote request.

### Unsafe remediation
Mitigation: there is no auto-remediation feature, shell-command execution, arbitrary Python evaluation, or cloud mutation workflow.

### Cloud credential misuse
Mitigation: use the standard AWS credential provider chain, prefer read-only roles, and do not paste secrets into source code or configuration. The initial project does not create IAM users or keys.

### Container privileges
Mitigation: the Docker image runs as a non-root user; Compose drops capabilities and does not mount the Docker socket. The current version does not inspect containers.

### Sensitive reports
Mitigation: reports contain derived summaries and evidence line numbers, not raw complete log files. Review exports before sharing them publicly.

## Residual risks

- Regex-based redaction is not comprehensive.
- Local reports may still contain sensitive error messages.
- A compromised Python dependency or host environment can affect the tool.
- AI responses can be wrong, biased, or manipulated.
- There is no authentication boundary in the local single-user dashboard.

Do not use this initial implementation as a production security control without an independent security review.
