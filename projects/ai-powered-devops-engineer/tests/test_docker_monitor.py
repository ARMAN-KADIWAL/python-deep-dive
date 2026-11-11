import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from devops_ai.monitoring.docker_monitor import DockerMonitor


def test_docker_monitor_rejects_unbounded_container_count():
    with pytest.raises(ValueError, match="max_containers"):
        DockerMonitor().list_statuses(max_containers=1000)


def test_docker_monitor_returns_limited_status_fields(monkeypatch):
    container = SimpleNamespace(
        attrs={"State": {"Health": {"Status": "healthy"}}},
        short_id="abcdef0123456789",
        name="orders",
        status="running",
        image=SimpleNamespace(tags=["orders:demo"]),
    )
    client = Mock()
    client.ping.return_value = True
    client.containers.list.return_value = [container]
    docker_module = SimpleNamespace(from_env=Mock(return_value=client))
    monkeypatch.setitem(sys.modules, "docker", docker_module)

    results = DockerMonitor(timeout_seconds=4).list_statuses(max_containers=10)

    assert results == [
        {
            "id": "abcdef0123456789",
            "name": "orders",
            "state": "running",
            "health": "healthy",
            "image": "orders:demo",
        }
    ]
    docker_module.from_env.assert_called_once_with(timeout=4)
    client.containers.list.assert_called_once_with(all=True, limit=10)
    client.close.assert_called_once()


def test_docker_monitor_hides_daemon_exception_details(monkeypatch):
    client = Mock()
    client.ping.side_effect = PermissionError("do not reveal local details")
    docker_module = SimpleNamespace(from_env=Mock(return_value=client))
    monkeypatch.setitem(sys.modules, "docker", docker_module)

    with pytest.raises(RuntimeError, match="PermissionError") as error:
        DockerMonitor().list_statuses()

    assert "do not reveal local details" not in str(error.value)
    client.close.assert_called_once()
