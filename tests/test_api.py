from fastapi.testclient import TestClient

from printclaw.web.app import app


def test_api_status_returns_200():
    client = TestClient(app)
    resp = client.get('/api/status')
    assert resp.status_code == 200
    assert resp.json()['status'] == 'ok'
