from devops_ai.analysis import analyze_events, fingerprint
from devops_ai.ingestion import parse_lines


def test_metrics_group_repeated_errors_and_detect_spike():
    lines = [
        "2026-10-15T10:00:00Z ERROR database connection refused",
        "2026-10-15T10:00:20Z ERROR database connection refused",
        "2026-10-15T10:00:40Z ERROR database connection refused",
        "2026-10-15T10:01:00Z WARNING cache refresh slow",
        "2026-10-15T10:01:20Z INFO request completed",
    ]
    events, rejected = parse_lines(lines, default_service="test")
    result = analyze_events(events, rejected_lines=rejected, error_spike_threshold=3)
    assert result["total_events"] == 5
    assert result["error_count"] == 3
    assert result["warning_count"] == 1
    assert result["error_rate_percent"] == 60.0
    assert any(item.category == "repeated-error" for item in result["findings"])
    assert any(item.category == "error-spike" for item in result["findings"])


def test_fingerprint_normalizes_variable_ip_and_ids():
    assert fingerprint("request_id=abc123 failed for 10.0.0.1") == fingerprint(
        "request_id=xyz987 failed for 10.0.0.2"
    )


def test_empty_analysis_has_zero_rate():
    result = analyze_events([])
    assert result["total_events"] == 0
    assert result["error_rate_percent"] == 0.0
    assert result["findings"] == []


def test_critical_finding_has_critical_severity():
    events, _ = parse_lines(["2026-10-15T10:00:00Z CRITICAL payment database unavailable"])
    result = analyze_events(events)
    assert any(item.severity == "CRITICAL" for item in result["findings"])
