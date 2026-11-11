"""Environment configuration with safe defaults."""

from __future__ import annotations

import os
from dataclasses import dataclass


def _positive_int(name: str, default: int, *, minimum: int = 1) -> int:
    try:
        value = int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default
    return value if value >= minimum else default


def _enabled(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    max_upload_bytes: int = 5 * 1024 * 1024
    error_spike_threshold: int = 5
    bedrock_enabled: bool = False
    aws_region: str = "ap-south-1"
    bedrock_model_id: str = ""

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            max_upload_bytes=_positive_int("MAX_UPLOAD_BYTES", 5 * 1024 * 1024, minimum=1024),
            error_spike_threshold=_positive_int("ERROR_SPIKE_THRESHOLD", 5),
            bedrock_enabled=_enabled("DEVOPS_AI_BEDROCK_ENABLED"),
            aws_region=os.getenv("AWS_REGION", "ap-south-1").strip() or "ap-south-1",
            bedrock_model_id=os.getenv("BEDROCK_MODEL_ID", "").strip(),
        )
