from fastapi.testclient import TestClient
from ReceiptsToLedger.main import app
import io

client = TestClient(app)

def test_e2e_flow(db_session):
    # Upload CSV
    csv_data = "value_date,description,amount,currency,external_id\n2025-01-10,INV-1001,100.00,USD,txn_e2e_1\n"
    files = {"file": ("test.csv", io.BytesIO(csv_data.encode()), "text/csv")}
    res = client.post("/transactions/upload", files=files)
    assert res.status_code == 200
    batch_id = res.json()["batch_id"]

    # Run matching
    res = client.post(f"/matches/run/{batch_id}")
    assert res.status_code == 200
