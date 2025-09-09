from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from io import StringIO
import csv
from fastapi.responses import StreamingResponse

from ReceiptsToLedger.core.db import get_db
from ReceiptsToLedger.api.deps import get_current_org
from ReceiptsToLedger.services.journal import build_journal

router = APIRouter()

@router.get("/{batch_id}")
def preview_journal(batch_id: str, db: Session = Depends(get_db), org_id: int = Depends(get_current_org)):
    return build_journal(batch_id, db, org_id)

@router.get("/{batch_id}/export")
def export_journal(batch_id: str, db: Session = Depends(get_db), org_id: int = Depends(get_current_org)):
    journal = build_journal(batch_id, db, org_id)
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Account", "Debit", "Credit", "Currency", "Reviewed By", "Reviewed At"])
    for e in journal["entries"]:
        writer.writerow([e["account"], e["debit"], e["credit"], e["currency"], e["reviewed_by"], e["reviewed_at"]])
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": f"attachment; filename=journal_{batch_id}.csv"})
