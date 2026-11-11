from unittest.mock import Mock

import pytest

from devops_ai.monitoring.cloudwatch import CloudWatchLogsReader


def test_cloudwatch_reader_maps_events_and_uses_configured_group():
    client = Mock()
    client.filter_log_events.return_value = {
        "events": [
            {
                "timestamp": 1792058400000,
                "message": "2026-10-15T10:00:00Z ERROR database connection refused",
                "eventId": "evt-1",
            }
        ]
    }
    reader = CloudWatchLogsReader(region="ap-south-1", client=client)
    events = reader.fetch_events(
        log_group_name="/app/orders",
        start_time_ms=1792050000000,
        end_time_ms=1792060000000,
        max_events=10,
    )
    assert len(events) == 1
    assert events[0].level == "ERROR"
    assert events[0].service == "/app/orders"
    client.filter_log_events.assert_called_once()
    assert client.filter_log_events.call_args.kwargs["logGroupName"] == "/app/orders"


def test_cloudwatch_reader_rejects_unbounded_request():
    reader = CloudWatchLogsReader(region="ap-south-1", client=Mock())
    with pytest.raises(ValueError, match="max_events"):
        reader.fetch_events(
            log_group_name="/app/orders",
            start_time_ms=100,
            end_time_ms=200,
            max_events=100_000,
        )


def test_cloudwatch_reader_follows_next_token_without_repeating():
    client = Mock()
    client.filter_log_events.side_effect = [
        {
            "events": [{"timestamp": 1792058400000, "message": "first"}],
            "nextToken": "next-1",
        },
        {"events": [{"timestamp": 1792058500000, "message": "second"}]},
    ]
    reader = CloudWatchLogsReader(region="ap-south-1", client=client)
    events = reader.fetch_events(
        log_group_name="/app/orders",
        start_time_ms=1792050000000,
        end_time_ms=1792060000000,
        max_events=10,
    )
    assert len(events) == 2
    assert client.filter_log_events.call_count == 2
