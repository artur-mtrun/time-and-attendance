from sqlalchemy import Column, Integer, String, Boolean
from .base import Base, TimestampMixin

class Employee(Base, TimestampMixin):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    enroll_number = Column(String(50), unique=True, nullable=False, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    card_number = Column(String(50))
    is_active = Column(Boolean, default=True) 