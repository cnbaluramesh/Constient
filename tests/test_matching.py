from ReceiptsToLedger.services.matching import run_matching
from ReceiptsToLedger.models.transaction import BankTransaction
from ReceiptsToLedger.models.invoice import Invoice
from datetime import date

def test_matching_logic(db_session):
    # Seed invoice + txn
    inv = Invoice(tenant_id=1, invoice_no="INV-1001", amount_due=100.0, currency="USD", issue_date=date.today(), organisation_id=1)
    db_session.add(inv)
    db_session.commit()
    txn = BankTransaction(value_date=date.today(), description="Payment for INV-1001", amount=100.0, currency="USD", batch_id="batch1", external_id="txn_1", organisation_id=1)
    db_session.add(txn)
    db_session.commit()

    matches = run_matching("batch1", db_session, matched_by="tester", org_id=1)
    assert len(matches) == 1
    assert matches[0].confidence_score >= 0.7
