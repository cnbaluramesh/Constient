from ReceiptsToLedger.core.celery_app import celery_app
from ReceiptsToLedger.services.matching import run_matching
from ReceiptsToLedger.core.db import SessionLocal

@celery_app.task
def run_matching_task(batch_id: str, matched_by: str = None, org_id: int = None):
    db = SessionLocal()
    try:
        matches = run_matching(batch_id, db, matched_by, org_id)
        return {"count": len(matches), "batch_id": batch_id}
    finally:
        db.close()
