from typing import List, Dict, Any
import requests
import logging
from app.core.config import settings
from app.services.terminal import TerminalService
from sqlalchemy.orm import Session
from requests.exceptions import Timeout, ConnectionError
from fastapi import HTTPException
from ..models.terminal import Terminal

# Konfiguracja loggera
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ZKTecoService:
    def __init__(self, db: Session):
        self.base_url = settings.ZKTECO_API_URL
        self.db = db
        self.timeout = 5  # 5 sekund timeoutu
        logger.debug(f"Inicjalizacja ZKTecoService z URL: {self.base_url}")
        
    def get_all_employees(self) -> List[Dict[Any, Any]]:
        """Pobiera wszystkich pracowników z API ZKTeco"""
        try:
            master_terminal = TerminalService.get_master_terminal(self.db)
            if not master_terminal:
                logger.error("Nie znaleziono czytnika wzorcowego w bazie")
                raise Exception("Nie znaleziono czytnika wzorcowego")
            
            logger.info(f"Znaleziono czytnik wzorcowy: IP={master_terminal.ip_address}, Port={master_terminal.port}")
            
            device_request = {
                "ipAddress": master_terminal.ip_address,
                "port": master_terminal.port,
                "deviceNumber": master_terminal.number
            }
            
            logger.debug(f"Wysyłam request do API ZKTeco: {device_request}")
            
            response = requests.post(
                f"{self.base_url}/api/Employee/get-all",
                json=device_request,
                timeout=self.timeout  # dodajemy timeout
            )
            
            logger.debug(f"Status odpowiedzi: {response.status_code}")
            logger.debug(f"Treść odpowiedzi: {response.text}")
            
            response_data = response.json()
            
            # Sprawdź strukturę odpowiedzi
            if isinstance(response_data, dict) and 'data' in response_data:
                employees_data = response_data['data']
                logger.info(f"Pobrano {len(employees_data)} pracowników z czytnika")
                return employees_data
            else:
                logger.error("Nieoczekiwana struktura odpowiedzi API")
                raise Exception("Nieoczekiwana struktura odpowiedzi API")
            
        except Timeout:
            raise HTTPException(
                status_code=504,
                detail="Timeout podczas połączenia z czytnikiem"
            )
        except ConnectionError:
            raise HTTPException(
                status_code=503,
                detail="Nie można połączyć się z czytnikiem"
            )
        except Exception as e:
            logger.error(f"Nieoczekiwany błąd: {str(e)}")
            raise 

    def send_employees_to_terminal(self, terminal: Any, employees: List[Any]) -> Dict:
        """
        Wysyła pracowników do terminala
        
        Args:
            terminal: Obiekt terminala z danymi połączenia
            employees: Lista pracowników do wysłania
        """
        try:
            logger.info(f"Wysyłanie pracowników do terminala: IP={terminal.ip_address}, Port={terminal.port}")
            
            results = []
            for emp in employees:
                payload = {
                    'ipAddress': terminal.ip_address,
                    'port': terminal.port,
                    'deviceNumber': terminal.number,
                    'enrollNumber': str(emp.enroll_number),
                    'name': emp.name,
                    'cardNumber': emp.card_number,
                    'password': '',  # Opcjonalne
                    'privilege': emp.privileges,
                    'enabled': emp.is_active
                }
                
                logger.debug(f"Wysyłam request do API ZKTeco dla pracownika {emp.enroll_number}: {payload}")
                
                response = requests.post(
                    f"{self.base_url}/api/Employee/save",
                    json=payload,
                    timeout=self.timeout
                )
                
                logger.debug(f"Status odpowiedzi: {response.status_code}")
                logger.debug(f"Treść odpowiedzi: {response.text}")
                
                if response.status_code != 200:
                    raise Exception(f"Błąd API ZKTeco dla pracownika {emp.enroll_number}: {response.text}")
                    
                results.append({
                    'employee_id': emp.id,
                    'enroll_number': emp.enroll_number,
                    'status': 'success'
                })
            
            return {
                'status': 'success',
                'message': f'Pomyślnie wysłano {len(results)} pracowników',
                'details': results
            }
                
        except Exception as e:
            logger.error(f"Błąd podczas wysyłania do terminala {terminal.ip_address}: {str(e)}")
            raise Exception(f"Błąd podczas wysyłania do terminala {terminal.ip_address}: {str(e)}")

    def get_attendance_from_terminal(self, terminal: Any) -> List[Dict[Any, Any]]:
        """Pobiera zdarzenia obecności z terminala"""
        try:
            logger.info(f"Pobieranie zdarzeń z terminala: IP={terminal.ip_address}, Port={terminal.port}")
            
            device_request = {
                "ipAddress": terminal.ip_address,
                "port": terminal.port,
                "deviceNumber": terminal.number
            }
            
            logger.debug(f"Wysyłam request do API ZKTeco: {device_request}")
            
            response = requests.post(
                f"{self.base_url}/api/Attendance/get-all-logs",
                json=device_request,
                timeout=self.timeout
            )
            
            logger.debug(f"Status odpowiedzi: {response.status_code}")
            logger.debug(f"Treść odpowiedzi: {response.text}")
            
            response_data = response.json()
            
            if isinstance(response_data, dict) and 'data' in response_data:
                attendance_data = response_data['data']
                logger.info(f"Surowe dane z czytnika: {attendance_data}")
                
                # Mapowanie pól z odpowiedzi API
                mapped_data = []
                for record in attendance_data:
                    mapped_record = {
                    'enrollNumber': record.get('userId', ''),  # Mapowanie userId na enrollNumber
                    'timestamp': record.get('logTime', ''),    # Mapowanie logTime na timestamp
                    'inOutMode': record.get('inOutMode', 0),
                    'verifyMode': record.get('verifyMode', 0),
                    'workCode': record.get('workCode', 0)
                    }
                    mapped_data.append(mapped_record)
                
                logger.info(f"Pobrano i zmapowano {len(mapped_data)} zdarzeń z czytnika")
                return mapped_data
                
            else:
                raise Exception("Nieoczekiwana struktura odpowiedzi API")
            
        except Exception as e:
            logger.error(f"Nieoczekiwany błąd: {str(e)}")
            raise

    def send_employees_batch(self, terminal: Any, employees: List[Any]) -> Dict:
        """
        Wysyła grupę pracowników do terminala za pomocą batch API
        
        Args:
            terminal: Obiekt terminala z danymi połączenia
            employees: Lista pracowników do wysłania
        """
        try:
            logger.info(f"Wysyłanie grupy pracowników do terminala: IP={terminal.ip_address}, Port={terminal.port}")
            
            # Przygotuj payload dla batch request
            employees_data = [{
                'enrollNumber': str(emp.enroll_number),
                'name': emp.name,
                'cardNumber': emp.card_number,
                'password': '',
                'privilege': emp.privileges,
                'enabled': emp.is_active
            } for emp in employees]
            
            payload = {
                'ipAddress': terminal.ip_address,
                'port': terminal.port,
                'deviceNumber': terminal.number,
                'employees': employees_data
            }
            
            logger.debug(f"Wysyłam batch request do API ZKTeco: {payload}")
            
            response = requests.post(
                f"{self.base_url}/api/Employee/save-batch",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                raise Exception(f"Błąd API ZKTeco podczas batch save: {response.text}")
            
            return {
                'status': 'success',
                'message': f'Pomyślnie wysłano {len(employees)} pracowników',
                'updated_count': len(employees)
            }
                
        except Exception as e:
            logger.error(f"Błąd podczas batch save do terminala {terminal.ip_address}: {str(e)}")
            raise

    def delete_employee(self, terminal: Terminal, enroll_number: str) -> Dict[str, Any]:
        """
        Usuwa pracownika z terminala
        """
        try:
            payload = {
                "ipAddress": terminal.ip_address,
                "port": terminal.port,
                "deviceNumber": terminal.number,
                "enrollNumber": str(enroll_number)
            }
            
            response = requests.post(
                f"{self.base_url}/api/Employee/delete",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                raise Exception(f"Błąd API ZKTeco: {response.text}")
            
            return response.json()
        except Exception as e:
            logger.error(f"Błąd podczas usuwania pracownika {enroll_number} z terminala: {str(e)}")
            raise