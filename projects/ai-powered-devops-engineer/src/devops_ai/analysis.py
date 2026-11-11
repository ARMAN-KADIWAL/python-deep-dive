"""Deterministic log analysis. No AI is required for these findings."""

from __future__ import annotations

import hashlib
import re
from collections import Counter, defaultdict
from datetime import datetime
from typing import Any

from devops_ai.models import Finding, LogEvent

_VOLATILE_PATTERNS = (
    re.compile(r"\b[0-9a-f]{8}-[0-9a-f-]{27,}\b", re.IGNORECASE),
    re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    re.compile(r"\brequest[_ -]?id[=: ]+[A-Za-z0-9_-]+\b", re.IGNORECASE),
    re.compile(r"\b0x[0-9a-f]+\b", re.IGNORECASE),
    re.compile(r"\b\d{4,}\b"),
)
SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "UNKNOWN": 4}


def fingerprint(message: str) -> str:
    normalized = message.lower().strip()
    for pattern in _VOLATILE_PATTERNS:
        normalized = pattern.sub("<variable>", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


def _time_range(events: list[LogEvent]) -> tuple[datetime | None, datetime | None]:
    stamps = [event.timestamp for event in events if event.timestamp is not None]
    return (min(stamps), max(stamps)) if stamps else (None, None)


def analyze_events(
    events: list[LogEvent], *, rejected_lines: int = 0, error_spike_threshold: int = 5
) -> dict[str, Any]:
    levels = Counter(event.level for event in events)
    total = len(events)
    errors = levels.get("ERROR", 0) + levels.get("CRITICAL", 0)
    warnings = levels.get("WARNING", 0)
    groups: dict[str, list[LogEvent]] = defaultdict(list)
    for event in events:
        groups[fingerprint(event.message)].append(event)

    findings: list[Finding] = []
    for key, grouped in groups.items():
        group_levels = {event.level for event in grouped}
        count = len(grouped)
        if "CRITICAL" in group_levels:
            severity = "CRITICAL"
        elif "ERROR" in group_levels:
            severity = "HIGH" if count >= 3 else "MEDIUM"
        elif "WARNING" in group_levels and count >= 2:
            severity = "MEDIUM"
        else:
            continue
        first, last = _time_range(grouped)
        representative = max(grouped, key=lambda event: len(event.message)).message
        findings.append(
            Finding(
                finding_id=key,
                category="repeated-error" if count > 1 else "log-error",
                severity=severity,
                summary=representative[:300],
                count=count,
                evidence_lines=[event.source_line for event in grouped[:20]],
                first_observed=first,
                last_observed=last,
                method="rule-based",
                limitations="Default severity rules do not account for business impact.",
            )
        )

    buckets: Counter[datetime] = Counter()
    events_by_bucket: dict[datetime, list[LogEvent]] = defaultdict(list)
    for event in events:
        if event.timestamp and event.level in {"ERROR", "CRITICAL"}:
            stamp = event.timestamp
            bucket = stamp.replace(minute=(stamp.minute // 5) * 5, second=0, microsecond=0)
            buckets[bucket] += 1
            events_by_bucket[bucket].append(event)
    for bucket, count in buckets.items():
        if count >= max(1, error_spike_threshold):
            selected = events_by_bucket[bucket]
            marker = hashlib.sha256(f"spike:{bucket.isoformat()}".encode()).hexdigest()[:16]
            findings.append(
                Finding(
                    finding_id=marker,
                    category="error-spike",
                    severity="HIGH",
                    summary=f"{count} error or critical events in the five-minute window starting {bucket.isoformat()}.",
                    count=count,
                    evidence_lines=[event.source_line for event in selected[:20]],
                    first_observed=bucket,
                    last_observed=selected[-1].timestamp,
                    method=f"rule-based; threshold={error_spike_threshold} errors per five minutes",
                    limitations="Threshold signal only; it does not establish statistical significance or root cause.",
                )
            )

    findings.sort(
        key=lambda item: (SEVERITY_ORDER.get(item.severity, 5), -item.count, item.summary)
    )
    first, last = _time_range(events)
    return {
        "total_events": total,
        "rejected_lines": rejected_lines,
        "error_count": errors,
        "warning_count": warnings,
        "critical_count": levels.get("CRITICAL", 0),
        "error_rate_percent": round(errors / total * 100, 2) if total else 0.0,
        "level_counts": dict(sorted(levels.items())),
        "service_counts": dict(Counter(event.service for event in events).most_common()),
        "findings": findings,
        "first_observed": first,
        "last_observed": last,
    }
