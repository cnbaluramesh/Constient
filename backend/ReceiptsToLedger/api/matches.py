from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ReceiptsToLedger.models.match import Match
from ReceiptsToLedger.core.db import get_db
from ReceiptsToLedger.api.deps import get_current_user, get_current_org
from ReceiptsToLedger.models.transaction import BankTransaction
from ReceiptsToLedger.services.matching import run_matching
from ReceiptsToLedger.services.tasks import run_matching_task
from ReceiptsToLedger.core.celery_app import celery_app

router = APIRouter()

@router.post("/run/{batch_id}")
def run_batch_matching(batch_id: str, db: Session = Depends(get_db), user=Depends(get_current_user), org_id: int = Depends(get_current_org)):
    matches = run_matching(batch_id, db, matched_by=user.email, org_id=org_id)
    return [{"id": m.id, "invoice_id": m.invoice_id, "confidence": m.confidence_score} for m in matches]

@router.post("/run_async/{batch_id}")
def run_batch_matching_async(batch_id: str, user=Depends(get_current_user), org_id: int = Depends(get_current_org)):
    task = run_matching_task.delay(batch_id, matched_by=user.email, org_id=org_id)
    return {"task_id": task.id, "status": "queued"}

@router.get("/status/{task_id}")
def get_task_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    return {"task_id": task_id, "status": task.status, "result": task.result}

@router.get("/batch/{batch_id}")
def get_batch_matches(batch_id: str, db: Session = Depends(get_db), org_id: int = Depends(get_current_org), skip: int = 0, limit: int = 20, status: str | None = None):
    # query = db.query(Match).filter(Match.organisation_id == org_id).join(Match.bank_txn).filter(Match.bank_txn.has(batch_id=batch_id))
    query = (
        db.query(Match)
        .join(BankTransaction, Match.bank_txn_id == BankTransaction.id)
        .filter(Match.organisation_id == org_id, BankTransaction.batch_id == batch_id)
)
    if status == "accepted":
        query = query.filter(Match.accepted == True)
    elif status == "rejected":
        query = query.filter(Match.accepted == False)
    elif status == "pending":
        query = query.filter(Match.accepted == None)

    matches = query.offset(skip).limit(limit).all()
    # return [{"id": m.id, "txn_id": m.bank_txn_id, "invoice_id": m.invoice_id, "confidence": m.confidence_score, "accepted": m.accepted, "reviewed_by": m.reviewed_by, "reviewed_at": m.reviewed_at} for m in matches]
    return [
        {
            "id": m.id,
            "txn_id": m.bank_txn_id,
            "invoice_id": m.invoice_id,
            "confidence": round(m.confidence_score, 2),
            "accepted": m.accepted if m.accepted is not None else False,
            "reviewed_by": m.reviewed_by or "",
            "reviewed_at": m.reviewed_at.isoformat() if m.reviewed_at else ""
        }
        for m in matches
    ]

@router.post("/{match_id}/accept")
def accept_match(match_id: int, db: Session = Depends(get_db), user=Depends(get_current_user), org_id: int = Depends(get_current_org)):
    match = db.query(Match).filter(Match.id == match_id, Match.organisation_id == org_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    match.accepted = True
    match.reviewed_by = user.email
    match.reviewed_at = datetime.utcnow()
    db.commit()
    return {"msg": "Match accepted"}

@router.post("/{match_id}/reject")
def reject_match(match_id: int, db: Session = Depends(get_db), user=Depends(get_current_user), org_id: int = Depends(get_current_org)):
    match = db.query(Match).filter(Match.id == match_id, Match.organisation_id == org_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    match.accepted = False
    match.reviewed_by = user.email
    match.reviewed_at = datetime.utcnow()
    db.commit()
    return {"msg": "Match rejected"}
