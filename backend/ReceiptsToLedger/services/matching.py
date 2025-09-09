from ReceiptsToLedger.models.transaction import BankTransaction
from ReceiptsToLedger.models.invoice import Invoice
from ReceiptsToLedger.models.match import Match
from sqlalchemy.orm import Session
from rapidfuzz import fuzz

def run_matching(batch_id: str, db: Session, matched_by: str = None, org_id: int = None):
    txns = db.query(BankTransaction).filter_by(batch_id=batch_id, organisation_id=org_id).all()
    invoices = db.query(Invoice).filter_by(organisation_id=org_id).all()
    results = []

    for txn in txns:
        best_score, best_invoice = 0, None
        for inv in invoices:
            score = 0.0
            # Rule 1: exact amount match
            if txn.amount == inv.amount_due and txn.currency == inv.currency:
                score += 0.7
            # Rule 2: fuzzy text match
            text_score = fuzz.partial_ratio(
                txn.description.lower(), f"{inv.invoice_no} {inv.tenant_id}".lower()
            ) / 100
            score += 0.3 * text_score
            if score > best_score:
                best_score, best_invoice = score, inv

        if best_invoice:
            match = Match(
                bank_txn_id=txn.id,
                invoice_id=best_invoice.id,
                confidence_score=round(best_score, 2),
                matched_by=matched_by,
                organisation_id=org_id,
            )
            db.add(match)
            db.commit()
            db.refresh(match)
            results.append(match)
    return results
