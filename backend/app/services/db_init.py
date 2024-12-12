from sqlalchemy.orm import Session
from ..models.user import User
from .auth import AuthService

def init_db(db: Session) -> None:
    """Initialize database with default admin user if no users exist"""
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(
            username="admin",
            hashed_password=AuthService.get_password_hash("admin"),
            is_active=True
        )
        db.add(admin)
        db.commit() 