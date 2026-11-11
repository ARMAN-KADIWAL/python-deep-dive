from datetime import UTC

import pytest

from devops_ai.ingestion import parse_lines, parse_log_bytes


def test_plain_text_parser_normalizes_timestamp_and_level():
    events, rejected = parse_lines(
        [
            "2026-10-15T10:00:00Z ERROR database connection refused",
            "2026-10-15T10:01:00Z INFO request completed",
        ]
    )
    assert rejected == 0
    assert len(events) == 2
    assert events[0].level == "ERROR"
    assert events[0].timestamp is not None
    assert events[0].timestamp.tzinfo == UTC


def test_json_lines_parser_and_malformed_json_count():
    events, rejected = parse_lines(
        [
            '{"timestamp":"2026-10-15T10:00:00Z","level":"ERROR","message":"db failed","service":"orders"}',
            '{"malformed":',
        ]
    )
    assert len(events) == 1
    assert events[0].service == "orders"
    assert events[0].level == "ERROR"
    assert rejected == 1


def test_naive_timestamp_is_treated_as_utc():
    events, rejected = parse_lines(["2026-10-15 10:00:00 WARNING slow dependency"])
    assert rejected == 0
    assert events[0].timestamp is not None
    assert events[0].timestamp.tzinfo == UTC


def test_upload_limit_is_enforced():
    with pytest.raises(ValueError, match="exceeds"):
        parse_log_bytes(b"0123456789", max_bytes=5)


def test_non_utf8_file_is_rejected():
    with pytest.raises(ValueError, match="UTF-8"):
        parse_log_bytes(b"\xff\xfe")
