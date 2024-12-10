from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.services.zkteco_service import ZKTecoService
import logging

logger = logging.getLogger(__name__)

# Cache na poziomie modułu
_sync_cache = {
    'raw_data': None,
    'to_add': [],
    'to_update': []
}

class EmployeeService:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def cache_sync_data(raw_data, to_add, to_update):
        """Zapisuje dane synchronizacji w pamięci podręcznej"""
        global _sync_cache
        _sync_cache = {
            'raw_data': raw_data,
            'to_add': to_add,
            'to_update': to_update
        }

    def sync_employees_with_reader(self):
        """Synchronizuje dane pracowników używając danych z cache"""
        try:
            global _sync_cache
            if not _sync_cache['raw_data']:
                raise Exception("Brak danych w cache. Najpierw wykonaj synchronizację.")
            
            logger.info("Używam danych z cache")
            
            # Używamy już przetworzonych list to_add i to_update
            for emp_data in _sync_cache['to_add']:
                try:
                    new_employee = Employee(
                        enroll_number=emp_data['enroll_number'],
                        name=emp_data['name'],
                        card_number=emp_data.get('card_number'),
                        privileges=emp_data.get('privileges', 0),
                        is_active=emp_data.get('is_active', True)
                    )
                    self.db.add(new_employee)
                    self.db.commit()
                except Exception as e:
                    logger.error(f"Błąd podczas dodawania pracownika: {str(e)}")
                    self.db.rollback()
                    raise

            for emp_data in _sync_cache['to_update']:
                try:
                    existing = self.get_employee_by_enroll_number(self.db, emp_data['enroll_number'])
                    if existing:
                        existing.name = emp_data['new']['name']
                        existing.card_number = emp_data['new']['card_number']
                        existing.privileges = emp_data['new']['privileges']
                        existing.is_active = emp_data['new']['is_active']
                        self.db.commit()
                except Exception as e:
                    logger.error(f"Błąd podczas aktualizacji pracownika: {str(e)}")
                    self.db.rollback()
                    raise

            result = {
                "added": len(_sync_cache['to_add']),
                "updated": len(_sync_cache['to_update']),
                "total": len(_sync_cache['to_add']) + len(_sync_cache['to_update'])
            }

            # Wyczyść cache po udanej synchronizacji
            _sync_cache['raw_data'] = None
            _sync_cache['to_add'] = []
            _sync_cache['to_update'] = []

            return result

        except Exception as e:
            logger.error(f"Błąd podczas synchronizacji z cache: {str(e)}")
            raise

    @staticmethod
    def get_employees(db: Session):
        try:
            employees = db.query(Employee).all()
            logger.debug(f"Pobrano {len(employees)} pracowników")
            return employees
        except Exception as e:
            logger.error(f"Błąd podczas pobierania pracowników: {str(e)}", exc_info=True)
            raise Exception(f"Błąd podczas pobierania pracowników: {str(e)}")

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

    def get_employees_from_reader(self):
        """Pobiera pracowników z czytnika wzorcowego"""
        zkteco_service = ZKTecoService(self.db)
        return zkteco_service.get_all_employees()

    def get_all_employees(self):
        """Pobiera pracowników z bazy danych"""
        return self.get_employees(self.db) 