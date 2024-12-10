from fastapi import APIRouter, Depends, HTTPException
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
        employee_service = EmployeeService(db)
        employees_data = employee_service.get_all_employees()
        
        # Przygotuj dane do zwrócenia
        to_add = []
        to_update = []
        
        for emp in employees_data['data']:
            existing = employee_service.get_employee_by_enroll_number(db, str(emp.get('enrollNumber')))
            if existing:
                to_update.append({
                    'old': {'name': existing.name},
                    'new': {'name': emp.get('name')},
                    'enroll_number': str(emp.get('enrollNumber')),
                    'card_number': emp.get('cardNumber'),
                    'privileges': emp.get('privilege', 0)
                })
            else:
                to_add.append({
                    'name': emp.get('name'),
                    'enroll_number': str(emp.get('enrollNumber')),
                    'card_number': emp.get('cardNumber'),
                    'privileges': emp.get('privilege', 0)
                })
        
        # Cache wszystkie potrzebne dane
        employee_service.cache_sync_data(employees_data, to_add, to_update)
        
        logger.info("Pobrano dane z czytnika wzorcowego")
        return {
            "message": "Znaleziono różnice w danych pracowników",
            "to_add": to_add,
            "to_update": to_update,
            "summary": {
                "new_employees": len(to_add),
                "modified_employees": len(to_update)
            }
        }
    except Exception as e:
        logger.error(f"Błąd podczas synchronizacji: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/sync-from-main/confirm")
def confirm_sync(db: Session = Depends(get_db)):
    """
    Zatwierdza zmiany używając danych z cache, bez ponownego łączenia z czytnikiem
    """
    try:
        logger.info("Rozpoczynam zapisywanie zmian z cache")
        employee_service = EmployeeService(db)
        
        # Używamy tylko danych z cache
        result = employee_service.sync_employees_with_reader()
        
        logger.info(f"Pomyślnie zsynchronizowano dane: {result}")
        return {
            "message": f"Pomyślnie zsynchronizowano {result['total']} pracowników",
            "details": result
        }
    except Exception as e:
        logger.error(f"Błąd podczas zatwierdzania synchronizacji: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 