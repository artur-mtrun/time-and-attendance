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

    @staticmethod
    def sync_employee(db: Session, zk_employee: dict):
        """Synchronizuje dane pracownika z czytnika z bazą danych"""
        try:
            # Mapowanie pól z API na model bazy danych
            employee_data = {
                "enroll_number": str(zk_employee.get('enrollNumber')),
                "name": zk_employee.get('name', ''),
                "password": zk_employee.get('password'),
                "card_number": zk_employee.get('cardNumber', ''),
                "privileges": zk_employee.get('privilege', 0),
                "is_active": zk_employee.get('enabled', True)
            }

            # Sprawdź czy pracownik już istnieje
            existing_employee = db.query(Employee).filter(
                Employee.enroll_number == employee_data['enroll_number']
            ).first()

            if existing_employee:
                # Aktualizuj istniejącego pracownika
                for key, value in employee_data.items():
                    setattr(existing_employee, key, value)
                db.commit()
                return existing_employee
            else:
                # Dodaj nowego pracownika
                new_employee = Employee(**employee_data)
                db.add(new_employee)
                db.commit()
                db.refresh(new_employee)
                return new_employee

        except Exception as e:
            db.rollback()
            raise Exception(f"Błąd podczas synchronizacji pracownika: {str(e)}") 