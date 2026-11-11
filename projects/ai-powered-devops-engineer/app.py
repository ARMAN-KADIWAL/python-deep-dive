"""Streamlit UI for local log triage and optional, consent-gated AI diagnosis."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import streamlit as st
from dotenv import load_dotenv

from devops_ai.ai.mock_provider import MockDiagnosisProvider
from devops_ai.ai.redaction import redact_evidence, redact_sensitive_text
from devops_ai.analysis import analyze_events
from devops_ai.config import Settings
from devops_ai.ingestion import parse_log_bytes
from devops_ai.reporting import build_report, to_json, to_markdown

PROJECT_DIR = Path(__file__).resolve().parent
load_dotenv(PROJECT_DIR / ".env", override=False)
SETTINGS = Settings.from_env()
SAMPLE_FILES = {
    "Normal operations": "application.log",
    "Database connection failure": "database_failure.log",
    "HTTP 5xx spike": "http_5xx_spike.log",
    "Prompt injection in log content": "prompt_injection.log",
}


def _safe_findings(analysis: dict[str, Any]) -> list[dict[str, Any]]:
    result = []
    for finding in analysis.get("findings", []):
        item = finding.to_dict()
        item["summary"] = redact_sensitive_text(str(item.get("summary", "")), max_chars=1000)
        result.append(item)
    return result


def _save_analysis(events: list[Any], rejected: int, source_name: str, threshold: int) -> None:
    analysis = analyze_events(
        events,
        rejected_lines=rejected,
        error_spike_threshold=threshold,
    )
    st.session_state["devops_analysis"] = analysis
    st.session_state["devops_events"] = events
    st.session_state["devops_source_name"] = source_name
    st.session_state.pop("devops_diagnosis", None)


st.set_page_config(
    page_title="AI-Powered DevOps Engineer",
    page_icon="🛠️",
    layout="wide",
)
st.title("AI-Powered DevOps Engineer")
st.caption("Evidence-first log triage with optional AI-assisted diagnosis.")
st.info(
    "This is a local-first portfolio project. Findings are rule-based; AI output is a hypothesis. "
    "No infrastructure is changed automatically."
)

with st.sidebar:
    st.header("Analysis settings")
    service_name = st.text_input("Default service name", value="application")[:200]
    spike_threshold = st.slider(
        "Error burst threshold (per five minutes)",
        min_value=1,
        max_value=30,
        value=min(30, max(1, SETTINGS.error_spike_threshold)),
    )
    st.caption(f"Maximum uploaded file size: {SETTINGS.max_upload_bytes // 1024 // 1024} MiB")
    st.divider()
    st.write("AI provider")
    bedrock_ready = SETTINGS.bedrock_enabled and bool(SETTINGS.bedrock_model_id)
    if bedrock_ready:
        st.success("Amazon Bedrock is configured; a separate consent checkbox is still required.")
        st.caption(f"Region: {SETTINGS.aws_region}")
    else:
        st.warning("Offline demo provider active. No language model is called.")
        st.caption("Set DEVOPS_AI_BEDROCK_ENABLED=true and BEDROCK_MODEL_ID to configure Bedrock.")

source_mode = st.radio(
    "Input source",
    ["Synthetic sample", "Upload a log file", "AWS CloudWatch Logs"],
    horizontal=True,
)
raw_content: bytes | None = None
source_name = "application.log"

if source_mode == "AWS CloudWatch Logs":
    st.subheader("Read-only CloudWatch Logs")
    st.warning(
        "This action calls the AWS CloudWatch Logs API and may incur AWS charges. "
        "It does not create or change AWS resources. Use an existing credential profile "
        "or IAM role with access restricted to the intended log group."
    )
    with st.form("cloudwatch_read_form"):
        log_group_name = st.text_input(
            "Existing CloudWatch log group name",
            placeholder="/aws/lambda/my-function",
        ).strip()
        lookback_minutes = st.slider(
            "Look back (minutes)", min_value=5, max_value=1440, value=60, step=5
        )
        approve_cloudwatch = st.checkbox(
            "I approve making a read-only AWS API request for this log group."
        )
        read_cloudwatch = st.form_submit_button("Fetch and analyze CloudWatch events")
    if read_cloudwatch:
        if not approve_cloudwatch:
            st.error("Confirm the read-only AWS request before proceeding.")
        elif not log_group_name:
            st.error("Enter an existing log group name.")
        else:
            try:
                from devops_ai.monitoring.cloudwatch import CloudWatchLogsReader

                end_time = datetime.now(UTC)
                start_time = end_time - timedelta(minutes=lookback_minutes)
                with st.spinner("Reading a bounded sample of CloudWatch events..."):
                    events = CloudWatchLogsReader(region=SETTINGS.aws_region).fetch_events(
                        log_group_name=log_group_name,
                        start_time_ms=int(start_time.timestamp() * 1000),
                        end_time_ms=int(end_time.timestamp() * 1000),
                        max_events=500,
                    )
                _save_analysis(
                    events,
                    rejected=0,
                    source_name=f"CloudWatch Logs: {log_group_name}",
                    threshold=spike_threshold,
                )
                st.success(f"Received {len(events)} CloudWatch events.")
                if not events:
                    st.info("No events were returned for this time range.")
            except Exception as exc:
                st.error(
                    f"CloudWatch request failed ({type(exc).__name__}). Check the Region, "
                    "log group, network access, and read-only IAM permissions. "
                    "No resources were created or changed."
                )
else:
    if source_mode == "Synthetic sample":
        sample_label = st.selectbox("Choose a scenario", list(SAMPLE_FILES.keys()))
        source_name = SAMPLE_FILES[sample_label]
        sample_path = PROJECT_DIR / "sample_data" / source_name
        try:
            raw_content = sample_path.read_bytes()
        except OSError:
            st.error("Sample file could not be read. Check the repository sample_data directory.")
    else:
        uploaded = st.file_uploader(
            "Upload .log, .txt, .jsonl, or .ndjson",
            type=["log", "txt", "jsonl", "ndjson"],
            max_upload_size=max(1, SETTINGS.max_upload_bytes // (1024 * 1024)),
        )
        if uploaded is not None:
            source_name = Path(uploaded.name).name
            raw_content = uploaded.getvalue()
            if len(raw_content) > SETTINGS.max_upload_bytes:
                st.error("File exceeds the configured upload limit.")
                raw_content = None

    if st.button("Analyze logs", type="primary", disabled=raw_content is None):
        try:
            events, rejected = parse_log_bytes(
                raw_content,
                max_bytes=SETTINGS.max_upload_bytes,
                default_service=service_name.strip() or "unknown",
            )
            _save_analysis(
                events,
                rejected=rejected,
                source_name=source_name,
                threshold=spike_threshold,
            )
            st.success(f"Analysis complete: {len(events)} events parsed.")
        except (ValueError, OSError) as exc:
            st.error(f"Unable to analyze this input: {exc}")

st.subheader("Optional Docker container status")
with st.expander("Inspect local Docker containers", expanded=False):
    st.write(
        "This integration reads container names, IDs, state, health, and image labels only. "
        "It does not read environment variables or container logs, execute commands, or change "
        "container state. Access to a Docker daemon/socket is highly privileged."
    )
    approve_docker = st.checkbox(
        "I approve querying the Docker daemon available to this Python process.",
        key="approve_docker_read",
    )
    if st.button("Refresh Docker status"):
        if not approve_docker:
            st.error("Confirm Docker inspection before querying the daemon.")
        else:
            try:
                from devops_ai.monitoring.docker_monitor import DockerMonitor

                with st.spinner("Reading Docker container status..."):
                    docker_rows = DockerMonitor().list_statuses(max_containers=50)
                st.session_state["devops_docker_rows"] = docker_rows
                st.session_state.pop("devops_docker_error", None)
            except Exception as exc:
                st.session_state["devops_docker_error"] = str(exc)
                st.session_state.pop("devops_docker_rows", None)
    if "devops_docker_error" in st.session_state:
        st.warning(st.session_state["devops_docker_error"])
        st.caption(
            'To enable the optional SDK, install with: pip install -e ".[dev,monitoring]". '
            "The Docker daemon must already be running and accessible."
        )
    elif "devops_docker_rows" in st.session_state:
        if st.session_state["devops_docker_rows"]:
            st.dataframe(st.session_state["devops_docker_rows"], use_container_width=True)
        else:
            st.info("Docker returned no containers.")

analysis = st.session_state.get("devops_analysis")
if analysis is None:
    st.subheader("Quick start")
    st.write(
        "Choose a synthetic incident and select Analyze logs, or explicitly approve a "
        "read-only CloudWatch request. Database and HTTP 5xx samples contain repeated failures."
    )
    st.stop()

st.subheader("Analysis overview")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Parsed events", analysis["total_events"])
m2.metric("Errors + critical", analysis["error_count"])
m3.metric("Warnings", analysis["warning_count"])
m4.metric("Error rate", f"{analysis['error_rate_percent']}%")
st.caption(f"Rejected non-empty lines: {analysis['rejected_lines']}")

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### Events by severity")
    if analysis["level_counts"]:
        st.bar_chart(analysis["level_counts"])
    else:
        st.write("No events were parsed.")
with col2:
    st.markdown("#### Events by service")
    if analysis["service_counts"]:
        st.bar_chart(analysis["service_counts"])
    else:
        st.write("No service values were available.")

st.subheader("Findings")
findings = _safe_findings(analysis)
if not findings:
    st.success("No findings matched the currently configured rules.")
else:
    st.dataframe(
        [
            {
                "Severity": item["severity"],
                "Category": item["category"],
                "Count": item["count"],
                "Summary": item["summary"],
                "Evidence lines": ", ".join(map(str, item["evidence_lines"])),
            }
            for item in findings
        ],
        use_container_width=True,
        hide_index=True,
    )
    with st.expander("Inspect finding evidence"):
        selected_finding = st.selectbox(
            "Finding",
            findings,
            format_func=lambda item: (
                f"{item['severity']} | {item['category']} | {item['summary'][:90]}"
            ),
        )
        st.json(selected_finding)

report = build_report(
    analysis,
    source_name=st.session_state.get("devops_source_name", "unknown"),
)
st.subheader("Export report")
col_json, col_md = st.columns(2)
with col_json:
    st.download_button(
        "Download JSON report",
        data=to_json(report),
        file_name="devops-incident-report.json",
        mime="application/json",
    )
with col_md:
    st.download_button(
        "Download Markdown report",
        data=to_markdown(report),
        file_name="devops-incident-report.md",
        mime="text/markdown",
    )

st.subheader("AI-assisted diagnosis")
st.write(
    "Diagnosis is optional. The offline provider offers a clearly labeled demonstration. "
    "Amazon Bedrock sends sanitized evidence outside this machine and may incur charges."
)
allow_bedrock = False
if bedrock_ready:
    allow_bedrock = st.checkbox(
        "I approve sending the sanitized findings shown below to Amazon Bedrock for diagnosis."
    )
    st.caption(
        "Only a bounded summary and findings are sent. Redaction is best-effort and cannot "
        "guarantee removal of every secret or personal detail. Review your logs before consenting."
    )

if st.button("Generate diagnosis"):
    evidence = {
        "source_name": st.session_state.get("devops_source_name", "unknown"),
        "summary": {
            "total_events": analysis["total_events"],
            "error_count": analysis["error_count"],
            "warning_count": analysis["warning_count"],
            "error_rate_percent": analysis["error_rate_percent"],
        },
        "findings": [
            {
                "category": item["category"],
                "severity": item["severity"],
                "summary": item["summary"],
                "count": item["count"],
                "evidence_lines": item["evidence_lines"],
            }
            for item in findings[:10]
        ],
    }
    safe_evidence = redact_evidence(evidence)
    try:
        if bedrock_ready and allow_bedrock:
            from devops_ai.ai.bedrock_provider import BedrockDiagnosisProvider

            provider = BedrockDiagnosisProvider(
                region=SETTINGS.aws_region,
                model_id=SETTINGS.bedrock_model_id,
            )
        else:
            provider = MockDiagnosisProvider()
        with st.spinner("Preparing diagnosis..."):
            st.session_state["devops_diagnosis"] = {
                "provider": provider.name,
                "result": provider.diagnose(safe_evidence),
            }
    except Exception as exc:
        st.session_state["devops_diagnosis"] = {
            "provider": "unavailable",
            "error": (
                f"{type(exc).__name__}: AI diagnosis unavailable. Core log analysis remains usable."
            ),
        }

diagnosis = st.session_state.get("devops_diagnosis")
if diagnosis:
    st.caption(f"Provider used: {diagnosis['provider']}")
    if "error" in diagnosis:
        st.error(diagnosis["error"])
    else:
        if diagnosis["provider"] == "offline-demo-provider":
            st.info("Offline demo only. No language model was called.")
        st.write(diagnosis["result"].get("summary", "No summary returned."))
        for index, hypothesis in enumerate(
            diagnosis["result"].get("possible_root_causes", []), start=1
        ):
            with st.expander(
                f"Hypothesis {index}: {hypothesis.get('description', 'Unspecified')[:100]}"
            ):
                st.write(f"Confidence: {hypothesis.get('confidence', 'LOW')}")
                st.write("Supporting evidence")
                st.write(hypothesis.get("supporting_evidence", []))
                st.write("Missing or contradictory evidence")
                st.write(hypothesis.get("missing_or_contradicting_evidence", []))
                st.write("Verification steps")
                st.write(hypothesis.get("verification_steps", []))
        st.write("Recommended investigation steps")
        st.write(diagnosis["result"].get("recommended_steps", []))
        st.caption(diagnosis["result"].get("limitations", ""))

st.divider()
st.caption(
    "Local analysis is deterministic. AI hypotheses need human verification. "
    "This application does not execute remediation commands or change cloud resources."
)
