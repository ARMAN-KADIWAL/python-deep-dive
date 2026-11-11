"""Typed data models shared by ingestion, analysis, and reporting."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class LogEvent:
    timestamp: datetime | None
    level: str
    message: str
    service: str = "unknown"
    source_line: int = 0
    http_status: int | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat() if self.timestamp else None
        return data


@dataclass(frozen=True)
class Finding:
    finding_id: str
    category: str
    severity: str
    summary: str
    count: int
    evidence_lines: list[int] = field(default_factory=list)
    first_observed: datetime | None = None
    last_observed: datetime | None = None
    method: str = "rule-based"
    limitations: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["first_observed"] = self.first_observed.isoformat() if self.first_observed else None
        data["last_observed"] = self.last_observed.isoformat() if self.last_observed else None
        return data
