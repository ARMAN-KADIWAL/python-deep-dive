"""Read-only, bounded CloudWatch Logs ingestion."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from devops_ai.ingestion import parse_lines
from devops_ai.models import LogEvent


class CloudWatchLogsReader:
    """Retrieve a bounded event sample from one explicitly configured log group."""

    def __init__(self, *, region: str, client: Any | None = None) -> None:
        if not region.strip():
            raise ValueError("AWS Region must not be empty.")
        self.region = region
        if client is None:
            import boto3
            from botocore.config import Config

            client = boto3.client(
                "logs",
                region_name=region,
                config=Config(
                    connect_timeout=5,
                    read_timeout=15,
                    retries={"max_attempts": 2, "mode": "standard"},
                ),
            )
        self.client = client

    def fetch_events(
        self,
        *,
        log_group_name: str,
        start_time_ms: int,
        end_time_ms: int,
        max_events: int = 500,
    ) -> list[LogEvent]:
        """Fetch up to 1,000 events. The method never creates or changes AWS resources."""
        if not log_group_name or not log_group_name.strip():
            raise ValueError("A CloudWatch log group name is required.")
        if start_time_ms < 0 or end_time_ms <= start_time_ms:
            raise ValueError("The time range is invalid.")
        if isinstance(max_events, bool) or not 1 <= max_events <= 1000:
            raise ValueError("max_events must be between 1 and 1,000.")

        collected: list[LogEvent] = []
        token: str | None = None
        seen_tokens: set[str] = set()
        while len(collected) < max_events:
            request: dict[str, Any] = {
                "logGroupName": log_group_name,
                "startTime": start_time_ms,
                "endTime": end_time_ms,
                "limit": min(1000, max_events - len(collected)),
            }
            if token:
                request["nextToken"] = token
            response = self.client.filter_log_events(**request)

            for item in response.get("events", []):
                message = str(item.get("message", ""))[:20_000]
                parsed, _ = parse_lines([message], default_service=log_group_name)
                fallback_timestamp = None
                try:
                    event_ms = int(item.get("timestamp"))
                    fallback_timestamp = datetime.fromtimestamp(event_ms / 1000, tz=UTC)
                except (TypeError, ValueError, OSError, OverflowError):
                    pass
                if parsed:
                    event = parsed[0]
                    timestamp = event.timestamp or fallback_timestamp
                    level = event.level
                    text = event.message
                    status = event.http_status
                else:
                    timestamp = fallback_timestamp
                    level = "UNKNOWN"
                    text = message
                    status = None
                collected.append(
                    LogEvent(
                        timestamp=timestamp,
                        level=level,
                        message=text,
                        service=log_group_name[:200],
                        source_line=len(collected) + 1,
                        http_status=status,
                    )
                )
                if len(collected) >= max_events:
                    break

            next_token = response.get("nextToken")
            if not next_token or next_token == token or next_token in seen_tokens:
                break
            seen_tokens.add(next_token)
            token = next_token
        return collected
