# Architecture

## Design

The initial release is a modular monolith. The dashboard calls local parsing, deterministic analysis, and reporting modules. Optional Bedrock diagnosis is invoked only after configuration and explicit consent.

~~~mermaid
flowchart TD
    U[Operator] --> UI[Streamlit Dashboard]
    UI --> V[Input Size and Format Validation]
    V --> P[Log Parser]
    P --> E[Normalized Log Events]
    E --> A[Deterministic Analysis Engine]
    A --> F[Evidence-backed Findings]
    F --> R[JSON and Markdown Reports]
    F --> C{Bedrock configured and consented?}
    C -->|No| M[Offline Demo Provider]
    C -->|Yes| S[Secret Redaction and Size Bound]
    S --> B[Amazon Bedrock Converse API]
    M --> D[Diagnosis Display]
    B --> D
    R --> UI
    D --> UI
~~~

## Request sequence

~~~mermaid
sequenceDiagram
    actor Operator
    participant UI as Streamlit UI
    participant Parser as Log Parser
    participant Engine as Analysis Engine
    participant Provider as Optional AI Provider
    participant Report as Report Exporter
    Operator->>UI: Select sample or upload log
    UI->>Parser: Validate size and parse
    Parser-->>UI: Events and rejected-line count
    UI->>Engine: Analyze normalized events
    Engine-->>UI: Metrics and findings with evidence
    Operator->>UI: Request diagnosis
    alt Bedrock configured and explicit consent given
        UI->>Provider: Send bounded, redacted evidence
        Provider-->>UI: Validated structured hypothesis
    else Offline mode
        UI->>Provider: Use local demo provider
        Provider-->>UI: Labeled demo output
    end
    Operator->>Report: Download report
    Report-->>Operator: JSON or Markdown
~~~

## Key decisions

- Deterministic findings are produced before AI diagnosis.
- Log lines are untrusted data, never executable instructions.
- AI output is a hypothesis, not confirmation of root cause.
- The app makes no automatic changes to servers, containers, IAM, or cloud resources.
- The first release uses session state and has no durable incident database.
- Docker and CloudWatch monitoring are separate follow-up milestones and are not yet part of the core implementation.

## Failure handling

- Invalid JSON records are counted as rejected input lines.
- Unclassified plain-text lines remain UNKNOWN events.
- Provider exceptions are caught by the UI and do not remove deterministic findings.
- Missing AWS configuration selects the offline demo provider.
- Upload limits and bounded AI evidence protect against unbounded inputs.
