"""Validation helpers for structured model-produced diagnosis JSON."""

from __future__ import annotations

import json
from typing import Any

CONFIDENCE_LEVELS = {"LOW", "MEDIUM", "HIGH"}


class InvalidDiagnosis(ValueError):
    """Raised when a model response does not match the expected shape."""


def parse_diagnosis(response_text: str) -> dict[str, Any]:
    text = response_text.strip()
    fence = chr(96) * 3
    if text.startswith(fence):
        text = text.removeprefix(fence + "json").removeprefix(fence)
        if text.rstrip().endswith(fence):
            text = text.rstrip()[: -len(fence)]
        text = text.strip()
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise InvalidDiagnosis("The AI response was not valid JSON.") from exc
    if not isinstance(payload, dict):
        raise InvalidDiagnosis("The AI response must be a JSON object.")

    summary = payload.get("summary")
    hypotheses = payload.get("possible_root_causes")
    recommendations = payload.get("recommended_steps")
    if not isinstance(summary, str) or not summary.strip():
        raise InvalidDiagnosis("Diagnosis is missing a summary.")
    if not isinstance(hypotheses, list):
        raise InvalidDiagnosis("possible_root_causes must be a list.")
    if not isinstance(recommendations, list) or not all(
        isinstance(item, str) for item in recommendations
    ):
        raise InvalidDiagnosis("recommended_steps must be a list of strings.")

    normalized_hypotheses = []
    for item in hypotheses:
        if not isinstance(item, dict):
            raise InvalidDiagnosis("Each root-cause hypothesis must be an object.")
        description = item.get("description")
        supporting = item.get("supporting_evidence", [])
        missing = item.get("missing_or_contradicting_evidence", [])
        confidence = item.get("confidence", "LOW")
        verification = item.get("verification_steps", [])
        for field_name, value in (
            ("supporting_evidence", supporting),
            ("missing_or_contradicting_evidence", missing),
            ("verification_steps", verification),
        ):
            if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
                raise InvalidDiagnosis(f"{field_name} must be a list of strings.")
        if not isinstance(description, str) or not description.strip():
            raise InvalidDiagnosis("A root-cause hypothesis needs a description.")
        if confidence not in CONFIDENCE_LEVELS:
            confidence = "LOW"
        normalized_hypotheses.append(
            {
                "description": description[:1000],
                "supporting_evidence": supporting[:10],
                "missing_or_contradicting_evidence": missing[:10],
                "confidence": confidence,
                "verification_steps": verification[:10],
            }
        )

    limitations = payload.get("limitations", "AI output is a hypothesis and must be verified.")
    if not isinstance(limitations, str):
        limitations = "AI output is a hypothesis and must be verified."
    return {
        "summary": summary[:3000],
        "possible_root_causes": normalized_hypotheses[:8],
        "recommended_steps": recommendations[:20],
        "limitations": limitations[:1000],
    }
