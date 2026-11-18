from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from slo_sentinel import SERVICE_NAME, __version__
from slo_sentinel.app import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


def test_health_returns_ok(client: TestClient) -> None:
    resp = client.get("/health")

    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("application/json")
    body = resp.json()
    assert body["status"] == "ok"
    assert body["service"] == SERVICE_NAME
    assert body["version"] == __version__


def test_health_time_is_current_utc(client: TestClient) -> None:
    body = client.get("/health").json()

    reported = datetime.fromisoformat(body["time"])
    assert reported.tzinfo is not None
    assert abs(datetime.now(UTC) - reported) < timedelta(seconds=5)


def test_unknown_route_is_404(client: TestClient) -> None:
    assert client.get("/does-not-exist").status_code == 404


def test_openapi_schema_lists_health(client: TestClient) -> None:
    schema = client.get("/api/openapi.json").json()
    assert "/health" in schema["paths"]