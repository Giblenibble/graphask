from fastapi.testclient import TestClient

from graphask.api.main import app
from graphask.config import Settings


def health_test():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_settings_load():
    assert Settings().database_url is not None
