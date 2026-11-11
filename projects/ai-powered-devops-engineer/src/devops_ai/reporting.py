"""Export analysis results as JSON or Markdown."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any


def _iso(value: Any) -> Any:
    return value.isoformat() if isinstance(value, datetime) else value


def build_report(analysis: dict[str, Any], *, source_name: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(),
        "source_name": source_name,
        "summary": {
            "total_events": analysis.get("total_events", 0),
            "rejected_lines": analysis.get("rejected_lines", 0),
            "error_count": analysis.get("error_count", 0),
            "warning_count": analysis.get("warning_count", 0),
            "critical_count": analysis.get("critical_count", 0),
            "error_rate_percent": analysis.get("error_rate_percent", 0.0),
            "first_observed": _iso(analysis.get("first_observed")),
            "last_observed": _iso(analysis.get("last_observed")),
        },
        "level_counts": analysis.get("level_counts", {}),
        "service_counts": analysis.get("service_counts", {}),
        "findings": [item.to_dict() for item in analysis.get("findings", [])],
        "limitations": [
            "Findings use deterministic parsing and configured rules.",
            "A finding does not prove a root cause.",
            "Timestamp-free events are excluded from time-window analysis.",
        ],
    }


def to_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True)


def to_markdown(report: dict[str, Any]) -> str:
    summary = report.get("summary", {})
    lines = [
        "# DevOps Log Analysis Report",
        "",
        f"- Generated at: {report.get('generated_at', 'unknown')}",
        f"- Source: {report.get('source_name', 'unknown')}",
        f"- Total events: {summary.get('total_events', 0)}",
        f"- Rejected lines: {summary.get('rejected_lines', 0)}",
        f"- Errors and critical events: {summary.get('error_count', 0)}",
        f"- Warnings: {summary.get('warning_count', 0)}",
        f"- Error rate: {summary.get('error_rate_percent', 0.0)}%",
        "",
        "## Findings",
        "",
    ]
    findings = report.get("findings", [])
    if not findings:
        lines.append("No findings were produced by the configured rules.")
    for finding in findings:
        lines.extend(
            [
                f"### {finding.get('severity', 'UNKNOWN')}: {finding.get('summary', 'Untitled finding')}",
                "",
                f"- Category: {finding.get('category', 'unknown')}",
                f"- Count: {finding.get('count', 0)}",
                f"- Method: {finding.get('method', 'unknown')}",
                f"- Evidence line numbers: {', '.join(map(str, finding.get('evidence_lines', []))) or 'not available'}",
                f"- Limitation: {finding.get('limitations', 'No limitation stated')}",
                "",
            ]
        )
    lines.extend(["## Limitations", ""])
    lines.extend(f"- {item}" for item in report.get("limitations", []))
    lines.append("")
    return "\n".join(lines)
