import os
import sys

from fastapi.testclient import TestClient

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "services"))
from service_a.app.main import app  # noqa: E402

client = TestClient(app)


def test_health() -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_compute_valid() -> None:
    resp = client.get("/compute", params={"n": 5})
    assert resp.status_code == 200
    assert resp.json() == {"input": 5, "result": 30}


def test_compute_invalid() -> None:
    resp = client.get("/compute", params={"n": -1})
    assert resp.status_code == 400
