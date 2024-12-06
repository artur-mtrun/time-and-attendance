from sqlalchemy.orm import Session
from app.models.user import User
from app.services.auth import get_password_hash

def init_db(db: Session) -> None:
    """Initialize database with default admin user if no users exist"""
    if not db.query(User).first():
        default_user = User(
            username="admin",
            password_hash=get_password_hash("admin"),
            is_admin=True
        )
        db.add(default_user)
        db.commit() 