from typing import Dict, Any
import logging
from sqlalchemy.orm import Session
from .zkteco_service import ZKTecoService
from .terminal import TerminalService
from .employee import EmployeeService

logger = logging.getLogger(__name__)

class SyncService:
    @staticmethod
    def sync_terminal(db: Session, terminal_id: int) -> Dict[str, Any]:
        """
        Synchronizuje pracowników między bazą danych a terminalem
        
        Args:
            db: Sesja bazy danych
            terminal_id: ID terminala do synchronizacji
            
        Returns:
            Dict zawierający statystyki synchronizacji
        """
        try:
            # Inicjalizacja serwisów
            zkteco_service = ZKTecoService(db)
            terminal = TerminalService.get_terminal(db, terminal_id)
            
            if not terminal:
                raise Exception(f"Nie znaleziono terminala o ID {terminal_id}")
                
            # Pobierz pracowników z terminala
            terminal_employees = zkteco_service.get_all_employees()
            
            # Pobierz pracowników z bazy danych
            db_employees = EmployeeService.get_all_employees(db)
            
            # Mapowanie pracowników
            terminal_emp_map = {str(emp['enrollNumber']): emp for emp in terminal_employees}
            db_emp_map = {str(emp.enroll_number): emp for emp in db_employees}
            
            employees_to_sync = []
            changes_details = []
            
            # Sprawdź pracowników do usunięcia (są w terminalu, ale nie ma ich w bazie)
            for terminal_emp in terminal_employees:
                if str(terminal_emp['enrollNumber']) not in db_emp_map:
                    # Usuń pracownika z terminala
                    zkteco_service.delete_employee(terminal, terminal_emp['enrollNumber'])
                    changes_details.append({
                        "employee": terminal_emp['name'],
                        "enroll_number": terminal_emp['enrollNumber'],
                        "type": "delete",
                        "message": "Usunięto pracownika z terminala (brak w bazie danych)"
                    })
            
            # Mapowanie pracowników z terminala po numerze ewidencyjnym
            terminal_emp_map = {str(emp['enrollNumber']): emp for emp in terminal_employees}
            
            # Znajdź pracowników do zaktualizowania/dodania
            employees_to_sync = []
            changes_details = []  # Szczegółowe informacje o zmianach
            
            for db_emp in db_employees:
                terminal_emp = terminal_emp_map.get(str(db_emp.enroll_number))
                
                
                # Zawsze dodaj pracownika do synchronizacji jeśli go nie ma w terminalu
                if not terminal_emp:
                    employees_to_sync.append(db_emp)
                    changes_details.append({
                        "employee": db_emp.name,
                        "enroll_number": db_emp.enroll_number,
                        "type": "add",
                        "message": "Dodano nowego pracownika do terminala"
                    })
                # Lub jeśli którekolwiek z jego danych się zmieniły
                elif (
                    terminal_emp['name'] != db_emp.name or
                    terminal_emp['cardNumber'] != db_emp.card_number or
                    terminal_emp['enabled'] != db_emp.is_active or
                    terminal_emp['privilege'] != db_emp.privileges
                ):
                    employees_to_sync.append(db_emp)
                    changes = []
                    if terminal_emp['name'] != db_emp.name:
                        changes.append(f"nazwa: {terminal_emp['name']} -> {db_emp.name}")
                    if terminal_emp['cardNumber'] != db_emp.card_number:
                        changes.append(f"karta: {terminal_emp['cardNumber']} -> {db_emp.card_number}")
                    if terminal_emp['enabled'] != db_emp.is_active:
                        changes.append(f"status: {terminal_emp['enabled']} -> {db_emp.is_active}")
                    if terminal_emp['privilege'] != db_emp.privileges:
                        changes.append(f"uprawnienia: {terminal_emp['privilege']} -> {db_emp.privileges}")
                    
                    changes_details.append({
                        "employee": db_emp.name,
                        "enroll_number": db_emp.enroll_number,
                        "type": "update",
                        "changes": changes
                    })
            
            # Wyślij zaktualizowanych pracowników do terminala
            if employees_to_sync:
                sync_result = zkteco_service.send_employees_batch(terminal, employees_to_sync)
            else:
                sync_result = {
                    'status': 'success',
                    'message': 'Brak pracowników do synchronizacji',
                    'updated_count': 0
                }
            
            # Zapisz zmiany w bazie danych
            db.commit()
            
            return {
                'terminal_id': terminal_id,
                'terminal_name': terminal.name,
                'total_employees': len(db_employees),
                'synced_employees': len(employees_to_sync),
                'sync_details': sync_result,
                'changes': changes_details  # Szczegółowe informacje o zmianach
            }
            
        except Exception as e:
            logger.error(f"Błąd podczas synchronizacji terminala {terminal_id}: {str(e)}")
            raise Exception(f"Błąd synchronizacji: {str(e)}")