"""Bounded log parser. Log content is data and is never executed."""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any

from devops_ai.models import LogEvent

TIMESTAMP_PREFIX = re.compile(r"^(?P<timestamp>\d{4}-\d{2}-\d{2}[T ][0-9:.+\-]+Z?)\s+(?P<body>.*)$")
LEVEL_PATTERN = re.compile(
    r"\b(DEBUG|INFO|NOTICE|WARN(?:ING)?|ERROR|ERR|CRITICAL|FATAL)\b", re.IGNORECASE
)
HTTP_STATUS_PATTERN = re.compile(r"\s(?P<status>[1-5]\d{2})\s+\d+(?:\s|$)")
LEVEL_MAP = {
    "DEBUG": "DEBUG",
    "INFO": "INFO",
    "NOTICE": "INFO",
    "WARN": "WARNING",
    "WARNING": "WARNING",
    "ERR": "ERROR",
    "ERROR": "ERROR",
    "CRITICAL": "CRITICAL",
    "FATAL": "CRITICAL",
}


def parse_timestamp(value: Any) -> datetime | None:
    """Parse ISO-like timestamps. Naive timestamps are treated as UTC."""
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _first(data: dict[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        value = data.get(key)
        if value is not None and value != "":
            return value
    return None


def _event_from_json(line: str, line_number: int, default_service: str) -> LogEvent | None:
    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    timestamp = parse_timestamp(_first(data, ("timestamp", "@timestamp", "time", "ts")))
    message = _first(data, ("message", "msg", "log", "event"))
    if message is None:
        message = json.dumps(data, ensure_ascii=False, sort_keys=True)
    level_value = _first(data, ("level", "severity", "log.level"))
    level_match = LEVEL_PATTERN.search(str(level_value or ""))
    level = LEVEL_MAP.get(level_match.group(1).upper(), "UNKNOWN") if level_match else "UNKNOWN"
    service = _first(data, ("service", "service_name", "application")) or default_service
    status_value = _first(data, ("status", "status_code", "http_status"))
    try:
        status = int(status_value) if status_value is not None else None
    except (TypeError, ValueError):
        status = None
    if status is not None and 500 <= status <= 599 and level == "UNKNOWN":
        level = "ERROR"
    elif status is not None and 400 <= status <= 499 and level == "UNKNOWN":
        level = "WARNING"
    return LogEvent(
        timestamp, level, str(message)[:20_000], str(service)[:200], line_number, status
    )


def _event_from_text(line: str, line_number: int, default_service: str) -> LogEvent | None:
    if not line.strip():
        return None
    timestamp = None
    body = line.strip()
    match = TIMESTAMP_PREFIX.match(body)
    if match:
        timestamp = parse_timestamp(match.group("timestamp"))
        body = match.group("body")
    level_match = LEVEL_PATTERN.search(body)
    level = LEVEL_MAP.get(level_match.group(1).upper(), "UNKNOWN") if level_match else "UNKNOWN"
    status_match = HTTP_STATUS_PATTERN.search(body)
    status = int(status_match.group("status")) if status_match else None
    if status is not None and 500 <= status <= 599 and level == "UNKNOWN":
        level = "ERROR"
    elif status is not None and 400 <= status <= 499 and level == "UNKNOWN":
        level = "WARNING"
    if not body:
        return None
    return LogEvent(timestamp, level, body[:20_000], default_service[:200], line_number, status)


def parse_lines(
    lines: Iterable[str], default_service: str = "unknown"
) -> tuple[list[LogEvent], int]:
    """Return parsed events and rejected non-empty lines."""
    events: list[LogEvent] = []
    rejected = 0
    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip("\r\n")
        if not line.strip():
            continue
        stripped = line.lstrip()
        if stripped.startswith("{"):
            event = _event_from_json(stripped, line_number, default_service)
            if event is None:
                rejected += 1
                continue
        else:
            event = _event_from_text(line, line_number, default_service)
            if event is None:
                rejected += 1
                continue
        events.append(event)
    return events, rejected


def parse_log_bytes(
    content: bytes, *, max_bytes: int = 5 * 1024 * 1024, default_service: str = "unknown"
) -> tuple[list[LogEvent], int]:
    if len(content) > max_bytes:
        raise ValueError(f"File exceeds the configured limit of {max_bytes} bytes.")
    try:
        decoded = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("The file must use UTF-8 text encoding.") from exc
    return parse_lines(decoded.splitlines(), default_service=default_service)
