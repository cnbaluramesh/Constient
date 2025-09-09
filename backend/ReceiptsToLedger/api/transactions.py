import csv
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from ReceiptsToLedger.models.transaction import BankTransaction
from ReceiptsToLedger.core.db import get_db
from ReceiptsToLedger.api.deps import get_current_user, get_current_org
from datetime import datetime

router = APIRouter()

@router.post("/upload")
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    org_id: int = Depends(get_current_org),
):
    content = await file.read()
    text = content.decode("utf-8").splitlines()
    reader = csv.DictReader(text)
    batch_id = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    for row in reader:
        if db.query(BankTransaction).filter_by(external_id=row["external_id"]).first():
            continue
        txn = BankTransaction(
            value_date=datetime.strptime(row["value_date"], "%Y-%m-%d"),
            description=row["description"],
            amount=float(row["amount"]),
            currency=row["currency"],
            batch_id=batch_id,
            external_id=row["external_id"],
            organisation_id=org_id,
        )
        db.add(txn)
    db.commit()
    return {"batch_id": batch_id}

@router.get("/batches")
def list_batches(db: Session = Depends(get_db), org_id: int = Depends(get_current_org)):
    rows = db.query(BankTransaction.batch_id).filter_by(organisation_id=org_id).distinct().all()
    return [r[0] for r in rows]

@router.get("/batch/{batch_id}")
def get_batch(batch_id: str, db: Session = Depends(get_db), org_id: int = Depends(get_current_org)):
    txns = db.query(BankTransaction).filter_by(batch_id=batch_id, organisation_id=org_id).all()
    return [
        {"id": t.id, "desc": t.description, "amount": t.amount, "currency": t.currency}
        for t in txns
    ]
