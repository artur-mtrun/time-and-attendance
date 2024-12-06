from sqlalchemy import Column, Integer, String, Boolean
from .base import Base, TimestampMixin

class Employee(Base, TimestampMixin):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    enroll_number = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    password = Column(String(20), nullable=True)
    card_number = Column(String(50))
    privileges = Column(Integer, default=0)
    is_active = Column(Boolean, default=True) 