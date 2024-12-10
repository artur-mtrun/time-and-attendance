from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from app.database import get_db
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.services.employee import EmployeeService
from app.services.zkteco_service import ZKTecoService
from app.services.terminal import TerminalService
import logging
from pydantic import BaseModel, validator, Field

# Konfiguracja loggera
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter(prefix="/employees", tags=["employees"])

class SendToTerminalsRequest(BaseModel):
    terminal_ids: List[int] = Field(alias="terminalIds")
    employee_ids: List[int] = Field(alias="employeeIds")

    class Config:
        allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "terminalIds": [1, 2],
                "employeeIds": [1, 2, 3]
            }
        }

    @validator('terminal_ids')
    def validate_terminal_ids(cls, v):
        if not v:
            raise ValueError("Lista terminal_ids nie może być pusta")
        return v

    @validator('employee_ids')
    def validate_employee_ids(cls, v):
        if not v:
            raise ValueError("Lista employee_ids nie może być pusta")
        return v

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
        
        # Cache dane do późniejszego użycia
        employee_service = EmployeeService(db)
        employee_service.cache_sync_data(employees_data, to_add, to_update)
        
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
        employee_service = EmployeeService(db)
        
        # Używamy danych z cache zamiast ponownego łączenia z czytnikiem
        result = employee_service.sync_employees_with_reader()
        
        logger.info(f"Pomyślnie zsynchronizowano dane: {result}")
        return {
            "message": f"Pomyślnie zsynchronizowano {result['total']} pracowników",
            "details": result
        }
        
    except Exception as e:
        logger.error(f"Błąd podczas zapisywania zmian: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/send-to-terminals")
def send_to_terminals(request: SendToTerminalsRequest, db: Session = Depends(get_db)):
    try:
        logger.info(f"Rozpoczynam wysyłanie pracowników do terminali: {request}")
        
        # Pobierz pracowników
        employees = []
        for emp_id in request.employee_ids:
            employee = EmployeeService.get_employee(db, emp_id)
            if employee:
                employees.append(employee)
            else:
                logger.warning(f"Nie znaleziono pracownika o ID {emp_id}")
        
        if not employees:
            raise HTTPException(
                status_code=400,
                detail="Nie znaleziono żadnego z wybranych pracowników"
            )
        
        # Przygotuj dane do wysłania
        zkteco_service = ZKTecoService(db)
        success_count = 0
        failed_count = 0
        results = []
        
        # Wysyłamy do każdego terminala
        for terminal_id in request.terminal_ids:
            try:
                terminal = TerminalService.get_terminal(db, terminal_id)
                if not terminal:
                    raise Exception(f"Nie znaleziono terminala o ID {terminal_id}")
                
                result = zkteco_service.send_employees_to_terminal(terminal, employees)
                success_count += 1
                results.append({
                    "terminal_id": terminal_id,
                    "status": "success",
                    "message": f"Wysłano {len(employees)} pracowników"
                })
            except Exception as e:
                failed_count += 1
                logger.error(f"Błąd podczas wysyłania do terminala {terminal_id}: {str(e)}")
                results.append({
                    "terminal_id": terminal_id,
                    "status": "error",
                    "message": str(e)
                })
        
        return {
            "message": f"Zakończono wysyłanie. Sukces: {success_count}, Błędy: {failed_count}",
            "details": results
        }
        
    except Exception as e:
        logger.error(f"Błąd podczas wysyłania do terminali: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 