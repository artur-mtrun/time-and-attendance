from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..services.sync_service import SyncService

router = APIRouter(tags=["sync"])

@router.post("/sync/attendance")
async def sync_attendance(db: Session = Depends(get_db)):
    return SyncService.sync_attendance_logs(db) 