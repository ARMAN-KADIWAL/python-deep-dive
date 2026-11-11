"""Read-only Docker container status inspection.

This module never reads container environments, executes in-container commands,
fetches logs, starts/stops containers, or mounts a Docker socket itself.
"""

from __future__ import annotations

import logging
from typing import Any


class DockerMonitor:
    """Read status from an already-running Docker daemon."""

    def __init__(self, *, timeout_seconds: int = 3) -> None:
        self.timeout_seconds = timeout_seconds

    def list_statuses(self, *, max_containers: int = 50) -> list[dict[str, Any]]:
        if isinstance(max_containers, bool) or not 1 <= max_containers <= 100:
            raise ValueError("max_containers must be between 1 and 100.")
        try:
            import docker
        except ImportError as exc:
            raise RuntimeError(
                "Docker SDK is not installed. Install the optional monitoring extra."
            ) from exc

        client = None
        try:
            client = docker.from_env(timeout=self.timeout_seconds)
            client.ping()
            containers = client.containers.list(all=True, limit=max_containers)
            results = []
            for container in containers:
                attributes = getattr(container, "attrs", {}) or {}
                state = attributes.get("State", {}) or {}
                health = state.get("Health", {}) or {}
                image_tags = getattr(getattr(container, "image", None), "tags", []) or []
                results.append(
                    {
                        "id": str(getattr(container, "short_id", ""))[:16],
                        "name": str(getattr(container, "name", "unknown"))[:200],
                        "state": str(getattr(container, "status", "unknown")),
                        "health": str(health.get("Status", "not-reported")),
                        "image": str(image_tags[0])[:200] if image_tags else "untagged",
                    }
                )
            return results
        except Exception as exc:
            raise RuntimeError(
                f"Docker status could not be read ({type(exc).__name__}). "
                "Check that Docker is running and that this user is authorized."
            ) from exc
        finally:
            if client is not None:
                try:
                    client.close()
                except Exception as exc:
                    logging.getLogger(__name__).debug(
                        "Docker client cleanup failed (%s).", type(exc).__name__
                    )
