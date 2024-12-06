from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.services.employee import EmployeeService

router = APIRouter(prefix="/employees", tags=["employees"])

@router.get("", response_model=List[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    return EmployeeService.get_employees(db)

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