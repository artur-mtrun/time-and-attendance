from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.services.employee import EmployeeService
from app.services.zkteco_service import ZKTecoService
import logging

# Konfiguracja loggera
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter(prefix="/employees", tags=["employees"])

@router.get("", response_model=List[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    try:
        return EmployeeService.get_employees(db)
    except Exception as e:
        logger.error(f"Błąd podczas pobierania pracowników: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Błąd podczas pobierania pracowników: {str(e)}"
        )

@router.post("", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    try:
        return EmployeeService.create_employee(db, employee)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = EmployeeService.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Pracownik nie znaleziony")
    return employee

@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, employee_data: EmployeeUpdate, db: Session = Depends(get_db)):
    employee = EmployeeService.update_employee(db, employee_id, employee_data)
    if not employee:
        raise HTTPException(status_code=404, detail="Pracownik nie znaleziony")
    return employee

@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    if not EmployeeService.delete_employee(db, employee_id):
        raise HTTPException(status_code=404, detail="Pracownik nie znaleziony")
    return {"message": "Pracownik został usunięty"}

@router.post("/sync-from-main")
def sync_employees_from_main(db: Session = Depends(get_db)):
    try:
        logger.info("Rozpoczynam synchronizację z czytnikiem wzorcowym")
        zkteco_service = ZKTecoService(db)
        employees_data = zkteco_service.get_all_employees()
        logger.debug(f"Pobrane dane z czytnika: {employees_data}")
        
        # Przeanalizuj różnice
        to_add = []
        to_update = []
        
        for zk_emp in employees_data:
            logger.debug(f"Przetwarzanie pracownika z czytnika: {zk_emp}")
            enroll_number = str(zk_emp.get('enrollNumber'))
            existing = EmployeeService.get_employee_by_enroll_number(db, enroll_number)
            logger.debug(f"Istniejący pracownik w bazie: {existing}")
            
            if existing:
                if (
                    zk_emp.get('name') != existing.name or
                    zk_emp.get('cardNumber') != existing.card_number or
                    zk_emp.get('privilege') != existing.privileges or
                    zk_emp.get('enabled', True) != existing.is_active
                ):
                    logger.info(f"Znaleziono różnice dla pracownika {enroll_number}")
                    to_update.append({
                        'enroll_number': enroll_number,
                        'old': {
                            'name': existing.name,
                            'card_number': existing.card_number,
                            'privileges': existing.privileges,
                            'is_active': existing.is_active
                        },
                        'new': {
                            'name': zk_emp.get('name'),
                            'card_number': zk_emp.get('cardNumber'),
                            'privileges': zk_emp.get('privilege'),
                            'is_active': zk_emp.get('enabled', True)
                        }
                    })
            else:
                logger.info(f"Znaleziono nowego pracownika {enroll_number}")
                to_add.append({
                    'enroll_number': enroll_number,
                    'name': zk_emp.get('name'),
                    'card_number': zk_emp.get('cardNumber'),
                    'privileges': zk_emp.get('privilege'),
                    'is_active': zk_emp.get('enabled', True)
                })

        result = {
            "message": "Znaleziono różnice w danych pracowników",
            "to_add": to_add,
            "to_update": to_update,
            "summary": {
                "new_employees": len(to_add),
                "modified_employees": len(to_update),
                "total_in_reader": len(employees_data),
                "total_in_db": len(EmployeeService.get_employees(db))
            }
        }
        logger.info(f"Wynik synchronizacji: {result}")
        return result

    except Exception as e:
        logger.error(f"Błąd podczas synchronizacji: {str(e)}")
        logger.exception("Szczegóły błędu:")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/sync-from-main/confirm")
def confirm_sync_employees(db: Session = Depends(get_db)):
    try:
        logger.info("Rozpoczynam zapisywanie zmian z synchronizacji")
        zkteco_service = ZKTecoService(db)
        employees_data = zkteco_service.get_all_employees()
        
        synced_count = 0
        for emp_data in employees_data:
            EmployeeService.sync_employee(db, emp_data)
            synced_count += 1
            
        return {
            "message": f"Pomyślnie zsynchronizowano {synced_count} pracowników"
        }
        
    except Exception as e:
        logger.error(f"Błąd podczas zapisywania zmian: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 