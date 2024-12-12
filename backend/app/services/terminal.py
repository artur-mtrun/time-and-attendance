from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import and_, or_
from app.models.terminal import Terminal
from app.schemas.terminal import TerminalCreate, TerminalUpdate
from fastapi import HTTPException

class TerminalService:
    @staticmethod
    def get_terminals(db: Session):
        return db.query(Terminal).all()

    @staticmethod
    def get_terminal(db: Session, terminal_id: int):
        return db.query(Terminal).filter(Terminal.id == terminal_id).first()

    @staticmethod
    def create_terminal(db: Session, terminal: TerminalCreate):
        if terminal.is_main and db.query(Terminal).filter(Terminal.is_main == True).first():
            raise HTTPException(
                status_code=400,
                detail="Może istnieć tylko jeden główny terminal. Najpierw odznacz istniejący główny terminal."
            )
            
        db_terminal = Terminal(**terminal.model_dump())
        db.add(db_terminal)
        db.commit()
        db.refresh(db_terminal)
        return db_terminal

    @staticmethod
    def update_terminal(db: Session, terminal_id: int, terminal_data: TerminalUpdate):
        db_terminal = TerminalService.get_terminal(db, terminal_id)
        if not db_terminal:
            return None

        update_data = terminal_data.model_dump(exclude_unset=True)
        
        if update_data.get('is_main'):
            existing_main = db.query(Terminal).filter(
                and_(
                    Terminal.is_main == True,
                    Terminal.id != terminal_id
                )
            ).first()
            
            if existing_main:
                raise HTTPException(
                    status_code=400,
                    detail="Może istnieć tylko jeden główny terminal. Najpierw odznacz istniejący główny terminal."
                )

        for key, value in update_data.items():
            setattr(db_terminal, key, value)
        
        db.commit()
        db.refresh(db_terminal)
        return db_terminal

    @staticmethod
    def delete_terminal(db: Session, terminal_id: int):
        db_terminal = TerminalService.get_terminal(db, terminal_id)
        if db_terminal:
            db.delete(db_terminal)
            db.commit()
            return True
        return False

    @staticmethod
    def sync_terminal(db: Session, terminal_id: int):
        db_terminal = TerminalService.get_terminal(db, terminal_id)
        if db_terminal:
            # Tutaj dodamy później faktyczną synchronizację z czytnikiem
            db_terminal.last_sync_at = datetime.utcnow()
            db.commit()
            db.refresh(db_terminal)
        return db_terminal

    @staticmethod
    def get_master_terminal(db: Session):
        """Pobiera czytnik wzorcowy z bazy danych"""
        return db.query(Terminal).filter(Terminal.is_main == True).first()

    @staticmethod
    def get_active_terminals(db: Session):
        terminals = db.query(Terminal).filter(Terminal.is_active == True).all()
        return terminals  # Zwracamy pustą listę zamiast rzucać wyjątek