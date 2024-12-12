from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..services.sync_service import SyncService
from ..dependencies.auth import oauth2_scheme

router = APIRouter(prefix="/api/sync", tags=["sync"])

@router.post("/dbsyncattendance")
async def dbsyncattendance(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Ręczna synchronizacja logów obecności między tabelami w bazie danych
    """
    try:
        result = SyncService.sync_attendance_logs(db)
        return {"status": "success", "message": result["message"]}
    except Exception as e:
        return {"status": "error", "message": str(e)} 