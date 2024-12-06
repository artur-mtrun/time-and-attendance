from fastapi import APIRouter
from app.api.endpoints import employees, terminals, users, attendance

api_router = APIRouter()

api_router.include_router(
    employees.router,
    prefix="/employees",
    tags=["employees"]
)

# ... inne routery ... 