"""Provider contract for optional AI diagnosis."""

from __future__ import annotations

from typing import Any, Protocol


class DiagnosisProvider(Protocol):
    name: str

    def diagnose(self, evidence: dict[str, Any]) -> dict[str, Any]:
        """Return a validated diagnosis from sanitized incident evidence."""
