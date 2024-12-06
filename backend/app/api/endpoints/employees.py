from fastapi import APIRouter, Depends, HTTPException
from app.services.zkteco_service import ZKTecoService
from app.services.employee import EmployeeService
from app.db.session import get_db
from sqlalchemy.orm import Session
import logging

# Konfiguracja loggera
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()

@router.get("/test")
def test_endpoint():
    return {"message": "Test endpoint działa"}

@router.post("/sync-from-main")
def sync_employees_from_main(db: Session = Depends(get_db)):
    try:
        logger.info("Rozpoczynam synchronizację z czytnikiem wzorcowym")
        zkteco_service = ZKTecoService(db)
        employees_data = zkteco_service.get_all_employees()
        logger.info("Pobrano dane z czytnika wzorcowego")
        return {"message": "Pomyślnie zsynchronizowano pracowników"}
    except Exception as e:
        logger.error(f"Błąd podczas synchronizacji: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 