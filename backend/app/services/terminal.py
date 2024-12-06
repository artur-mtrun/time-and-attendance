from sqlalchemy.orm import Session
from datetime import datetime
from app.models.terminal import Terminal
from app.schemas.terminal import TerminalCreate, TerminalUpdate

class TerminalService:
    @staticmethod
    def get_terminals(db: Session):
        return db.query(Terminal).all()

    @staticmethod
    def get_terminal(db: Session, terminal_id: int):
        return db.query(Terminal).filter(Terminal.id == terminal_id).first()

    @staticmethod
    def create_terminal(db: Session, terminal: TerminalCreate):
        db_terminal = Terminal(**terminal.model_dump())
        db.add(db_terminal)
        db.commit()
        db.refresh(db_terminal)
        return db_terminal

    @staticmethod
    def update_terminal(db: Session, terminal_id: int, terminal_data: TerminalUpdate):
        db_terminal = TerminalService.get_terminal(db, terminal_id)
        if db_terminal:
            update_data = terminal_data.model_dump(exclude_unset=True)
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