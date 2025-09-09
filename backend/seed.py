from ReceiptsToLedger.core.db import SessionLocal, engine, Base
from ReceiptsToLedger.models.organisation import Organisation
from ReceiptsToLedger.models.user import User, Role
from ReceiptsToLedger.models.tenant import Tenant
from ReceiptsToLedger.models.invoice import Invoice
from ReceiptsToLedger.core.security import hash_password
from datetime import date

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # One organisation
    org = Organisation(name="OrgA")
    db.add(org)
    db.commit()

    # Users
    admin = User(email="admin@orga.com", hashed_password=hash_password("password"), role=Role.admin, organisation_id=org.id)
    analyst = User(email="analyst@orga.com", hashed_password=hash_password("password"), role=Role.analyst, organisation_id=org.id)
    db.add_all([admin, analyst])
    db.commit()

    # Tenants
    acme = Tenant(name="ACME Corp", email="billing@acme.com", organisation_id=org.id)
    john = Tenant(name="John Doe Holdings", email="john@johndoe.com", organisation_id=org.id)
    mega = Tenant(name="Megacorp", email="ap@megacorp.com", organisation_id=org.id)
    db.add_all([acme, john, mega])
    db.commit()

    # Invoices
    invoices = [
        Invoice(tenant_id=acme.id, invoice_no="INV-1007", amount_due=1200.0, currency="USD", issue_date=date(2025, 1, 1), organisation_id=org.id),
        Invoice(tenant_id=john.id, invoice_no="INV-1002", amount_due=800.0, currency="USD", issue_date=date(2025, 1, 3), organisation_id=org.id),
        Invoice(tenant_id=mega.id, invoice_no="INV-1009", amount_due=950.0, currency="USD", issue_date=date(2025, 1, 5), organisation_id=org.id),
    ]
    db.add_all(invoices)
    db.commit()

    db.close()
    print("✅ Seed complete: OrgA with users, tenants, invoices.")

if __name__ == "__main__":
    seed()
