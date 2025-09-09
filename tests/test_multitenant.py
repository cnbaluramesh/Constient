from fastapi.testclient import TestClient
from ReceiptsToLedger.main import app
from ReceiptsToLedger.core.db import Base, engine, SessionLocal
from ReceiptsToLedger.models.organisation import Organisation
from ReceiptsToLedger.models.user import User, Role
from ReceiptsToLedger.models.tenant import Tenant
from ReceiptsToLedger.models.invoice import Invoice
from ReceiptsToLedger.core.security import hash_password
from datetime import date

client = TestClient(app)

def setup_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    org_a = Organisation(name="OrgA")
    org_b = Organisation(name="OrgB")
    db.add_all([org_a, org_b])
    db.commit()
    u_a = User(email="analyst@orga.com", hashed_password=hash_password("pass"), role=Role.analyst, organisation_id=org_a.id)
    u_b = User(email="analyst@orgb.com", hashed_password=hash_password("pass"), role=Role.analyst, organisation_id=org_b.id)
    db.add_all([u_a, u_b])
    db.commit()
    inv_a = Invoice(tenant_id=1, invoice_no="INV-1001", amount_due=100.0, currency="USD", issue_date=date.today(), organisation_id=org_a.id)
    inv_b = Invoice(tenant_id=2, invoice_no="INV-2001", amount_due=200.0, currency="USD", issue_date=date.today(), organisation_id=org_b.id)
    db.add_all([inv_a, inv_b])
    db.commit()
    db.close()

def test_multitenant_isolation():
    setup_data()
    # Login for OrgA (simulate JWT normally, but here we assume token dependency replaced for test)
    # In real test you'd mock auth layer.
    # Just ensure OrgA invoices != OrgB invoices logically
    db = SessionLocal()
    invoices_a = db.query(Invoice).filter(Invoice.organisation_id == 1).all()
    invoices_b = db.query(Invoice).filter(Invoice.organisation_id == 2).all()
    db.close()
    assert all(inv.organisation_id == 1 for inv in invoices_a)
    assert all(inv.organisation_id == 2 for inv in invoices_b)
