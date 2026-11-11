"""Best-effort redaction for common secrets before optional external AI calls."""

from __future__ import annotations

import re
from typing import Any

_PATTERNS = (
    (re.compile(r"(?i)\b(authorization\s*[:=]\s*bearer)\s+[A-Za-z0-9._~+/\-=]+"), r"\1 [REDACTED]"),
    (
        re.compile(
            r"(?i)\b(password|passwd|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*([^\s,;]+)"
        ),
        r"\1=[REDACTED]",
    ),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "[REDACTED_AWS_ACCESS_KEY]"),
    (
        re.compile(
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.DOTALL
        ),
        "[REDACTED_PRIVATE_KEY]",
    ),
)
_SENSITIVE_KEY = re.compile(
    r"(?i)(password|passwd|secret|api[_-]?key|access[_-]?token|authorization|client[_-]?secret|private[_-]?key)"
)


def redact_sensitive_text(value: str, *, max_chars: int = 12_000) -> str:
    text = value[:max_chars]
    for pattern, replacement in _PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def redact_evidence(value: Any) -> Any:
    """Redact sensitive dictionary fields and patterns inside text values."""
    if isinstance(value, dict):
        cleaned = {}
        for key, item in value.items():
            if _SENSITIVE_KEY.search(str(key)):
                cleaned[str(key)] = "[REDACTED]"
            else:
                cleaned[str(key)] = redact_evidence(item)
        return cleaned
    if isinstance(value, list):
        return [redact_evidence(item) for item in value[:100]]
    if isinstance(value, str):
        return redact_sensitive_text(value)
    if value is None or isinstance(value, (int, float, bool)):
        return value
    return redact_sensitive_text(str(value))
