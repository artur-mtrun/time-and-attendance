# Dokumentacja API ZK Teco

## Podstawowe informacje
- Base URL: `http://10.0.1.38:5000`
- Dokumentacja Swagger: `/swagger/index.html`

## Endpointy

### Attendance
- **POST /api/Attendance/get-logs**: Pobiera logi obecności.
- **POST /api/Attendance/get-all-logs**: Pobiera wszystkie logi obecności.

### Device
- **GET /api/Device/connect**: Łączy się z urządzeniem.
  - Parametry: `ip` (string), `port` (integer, default: 4370)
- **GET /api/Device/disconnect**: Rozłącza się z urządzeniem.
- **POST /api/Device/set-time**: Ustawia czas na urządzeniu.
- **POST /api/Device/get-info**: Pobiera informacje o urządzeniu.

### Employee
- **POST /api/Employee/get-info**: Pobiera informacje o pracowniku.
- **POST /api/Employee/get-all**: Pobiera informacje o wszystkich pracownikach.
- **POST /api/Employee/save**: Zapisuje informacje o pracowniku.
- **POST /api/Employee/change-enroll**: Zmienia numer rejestracyjny pracownika.

### Fingerprint
- **POST /api/Fingerprint/get**: Pobiera dane odcisku palca.
- **POST /api/Fingerprint/set**: Ustawia dane odcisku palca.
- **POST /api/Fingerprint/bulk-set**: Ustawia dane odcisków palców dla wielu użytkowników.

### Log
- **POST /api/Log/operations**: Pobiera logi operacji.

### ZkemAPI.Web
- **GET /**: Strona główna API.

## Przykłady użycia
*(do uzupełnienia)*

## Znane ograniczenia
*(do uzupełnienia)* 