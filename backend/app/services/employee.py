from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

class EmployeeService:
    @staticmethod
    def get_employees(db: Session):
        return db.query(Employee).all()

    @staticmethod
    def get_employee(db: Session, employee_id: int):
        return db.query(Employee).filter(Employee.id == employee_id).first()

    @staticmethod
    def get_employee_by_enroll_number(db: Session, enroll_number: str):
        return db.query(Employee).filter(Employee.enroll_number == enroll_number).first()

    @staticmethod
    def create_employee(db: Session, employee: EmployeeCreate):
        # Sprawdź czy pracownik o takim numerze już istnieje
        existing_employee = EmployeeService.get_employee_by_enroll_number(db, employee.enroll_number)
        if existing_employee:
            raise ValueError("Pracownik o takim numerze już istnieje")

        db_employee = Employee(**employee.model_dump())
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee

    @staticmethod
    def update_employee(db: Session, employee_id: int, employee_data: EmployeeUpdate):
        db_employee = EmployeeService.get_employee(db, employee_id)
        if db_employee:
            update_data = employee_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_employee, key, value)
            db.commit()
            db.refresh(db_employee)
        return db_employee

    @staticmethod
    def delete_employee(db: Session, employee_id: int):
        db_employee = EmployeeService.get_employee(db, employee_id)
        if db_employee:
            db.delete(db_employee)
            db.commit()
            return True
        return False 