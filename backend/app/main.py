from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, users, terminals, employees, attendance
from app.database import engine, SessionLocal
from app.services.db_init import init_db

app = FastAPI()

# Konfiguracja CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dodaj router autentykacji
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(terminals.router, prefix="/api")
app.include_router(employees.router, prefix="/api")
app.include_router(attendance.router, prefix="/api")

# Inicjalizacja bazy danych
init_db(SessionLocal())

@app.get("/")
async def read_root():
    return {"Hello": "World"}