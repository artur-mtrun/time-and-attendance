from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..services.sync_service import SyncService
from ..dependencies.auth import oauth2_scheme

router = APIRouter(prefix="/api/sync", tags=["sync"])

@router.post("/dbsyncattendance")
def sync_attendance(db: Session = Depends(get_db)):
    """
    Endpoint do synchronizacji logów obecności.
    
    Args:
        db (Session): Sesja bazy danych wstrzykiwana przez FastAPI
        
    Returns:
        dict: Słownik zawierający:
            - status: Status operacji ("success" lub "error")
            - message: Komunikat opisujący wynik operacji
            - statystyki: Szczegółowe statystyki synchronizacji zawierające:
                - przetworzone_rekordy: Liczba wszystkich przetworzonych rekordów
                - dodane_nowe: Liczba nowo dodanych rekordów
                - już_istniejące: Liczba rekordów, które już istniały
                - bez_pracownika: Liczba rekordów bez przypisanego pracownika
    
    Raises:
        HTTPException: W przypadku błędu podczas synchronizacji
    """
    try:
        result = SyncService.sync_attendance_logs(db)
        return {
            "status": "success",
            "message": result["message"],
            "statystyki": result["statystyki"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 