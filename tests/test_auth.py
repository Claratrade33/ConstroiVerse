import json
from backend.app import app

def test_health():
    c = app.test_client()
    r = c.get('/health')
    assert r.status_code == 200
    assert r.json.get('status') == 'ok'