from sqlalchemy.orm import Session
from sqlalchemy import func
from ReceiptsToLedger.models.transaction import BankTransaction
from ReceiptsToLedger.models.invoice import Invoice
from ReceiptsToLedger.models.match import Match

def build_journal(batch_id: str, db: Session, org_id: int):
    rows = (
        db.query(
            Invoice.tenant_id,
            func.sum(BankTransaction.amount).label("amount"),
            BankTransaction.currency,
            func.min(Match.reviewed_by).label("reviewed_by"),
            func.min(Match.reviewed_at).label("reviewed_at"),
        )
        .join(Match, Match.invoice_id == Invoice.id)
        .join(BankTransaction, Match.bank_txn_id == BankTransaction.id)
        .filter(BankTransaction.batch_id == batch_id)
        .filter(BankTransaction.organisation_id == org_id)
        .filter(Match.accepted == True)
        .group_by(Invoice.tenant_id, BankTransaction.currency)
        .all()
    )

    journal_entries, total_debit = [], 0
    for tenant_id, amount, currency, reviewer, reviewed_at in rows:
        journal_entries.append({
            "account": f"Accounts Receivable - Tenant {tenant_id}",
            "debit": 0.0,
            "credit": float(amount),
            "currency": currency,
            "reviewed_by": reviewer,
            "reviewed_at": str(reviewed_at) if reviewed_at else None,
        })
        total_debit += float(amount)

    if total_debit > 0:
        journal_entries.append({
            "account": "Cash",
            "debit": total_debit,
            "credit": 0.0,
            "currency": rows[0].currency if rows else "USD",
            "reviewed_by": None,
            "reviewed_at": None,
        })

    total_credits = sum(e["credit"] for e in journal_entries)
    total_debits = sum(e["debit"] for e in journal_entries)
    balanced = abs(total_debits - total_credits) < 0.01

    return {
        "batch_id": batch_id,
        "entries": journal_entries,
        "total_debits": total_debits,
        "total_credits": total_credits,
        "balanced": balanced,
    }
