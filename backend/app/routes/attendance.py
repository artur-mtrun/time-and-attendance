from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from app.database import get_db
from app.schemas.attendance import AttendanceResponse, AttendanceCreate
from app.services.attendance import AttendanceService

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.get("", response_model=List[AttendanceResponse])
def get_attendance_logs(
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    db: Session = Depends(get_db)
):
    if not start_date:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if not end_date:
        end_date = start_date + timedelta(days=1)

    return AttendanceService.get_attendance_logs(db, start_date, end_date)

@router.get("/employee/{employee_id}", response_model=List[AttendanceResponse])
def get_employee_attendance(
    employee_id: int,
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    db: Session = Depends(get_db)
):
    return AttendanceService.get_employee_attendance(db, employee_id, start_date, end_date)

@router.post("", response_model=AttendanceResponse)
def create_attendance_log(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):
    return AttendanceService.create_attendance_log(db, attendance) 