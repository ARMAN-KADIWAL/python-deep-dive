import json

from devops_ai.analysis import analyze_events
from devops_ai.ingestion import parse_lines
from devops_ai.reporting import build_report, to_json, to_markdown


def test_json_and_markdown_reports_include_findings():
    events, rejected = parse_lines(
        [
            "2026-10-15T10:00:00Z ERROR database connection refused",
            "2026-10-15T10:00:20Z ERROR database connection refused",
        ]
    )
    report = build_report(
        analyze_events(events, rejected_lines=rejected),
        source_name="synthetic-test.log",
    )
    parsed = json.loads(to_json(report))
    markdown = to_markdown(report)
    assert parsed["summary"]["total_events"] == 2
    assert parsed["source_name"] == "synthetic-test.log"
    assert "Findings" in markdown
    assert "database connection refused" in markdown
