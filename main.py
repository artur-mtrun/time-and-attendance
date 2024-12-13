from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, attendance_all  # Przykład importu routerów

app = FastAPI()

# Lista dozwolonych originów
origins = [
    "http://localhost:3000",  # Przykład dla React/Vue na porcie 3000
    "http://your-frontend-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Możesz użyć ["*"] dla wszystkich originów (niezalecane w produkcji)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(attendance_all.router)

# ... reszta kodu aplikacji 