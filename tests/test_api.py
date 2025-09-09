from fastapi.testclient import TestClient
from ReceiptsToLedger.main import app

client = TestClient(app)

def test_healthcheck():
    res = client.get("/healthcheck")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
