from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.terminal import TerminalCreate, TerminalResponse, TerminalUpdate
from app.services.terminal import TerminalService
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/terminals", 
    tags=["terminals"],
    dependencies=[Depends(get_current_user)]
)

@router.get("", response_model=List[TerminalResponse])
def get_terminals(db: Session = Depends(get_db)):
    return TerminalService.get_terminals(db)

@router.post("", response_model=TerminalResponse)
def create_terminal(terminal: TerminalCreate, db: Session = Depends(get_db)):
    return TerminalService.create_terminal(db, terminal)

@router.get("/active", response_model=List[TerminalResponse])
def get_active_terminals(db: Session = Depends(get_db)):
    terminals = TerminalService.get_active_terminals(db)
    if not terminals:
        return []
    return terminals

@router.get("/{terminal_id}", response_model=TerminalResponse)
def get_terminal(terminal_id: int, db: Session = Depends(get_db)):
    terminal = TerminalService.get_terminal(db, terminal_id)
    if not terminal:
        raise HTTPException(status_code=404, detail="Terminal not found")
    return terminal

@router.put("/{terminal_id}", response_model=TerminalResponse)
def update_terminal(terminal_id: int, terminal_data: TerminalUpdate, db: Session = Depends(get_db)):
    terminal = TerminalService.update_terminal(db, terminal_id, terminal_data)
    if not terminal:
        raise HTTPException(status_code=404, detail="Terminal not found")
    return terminal

@router.delete("/{terminal_id}")
def delete_terminal(terminal_id: int, db: Session = Depends(get_db)):
    if not TerminalService.delete_terminal(db, terminal_id):
        raise HTTPException(status_code=404, detail="Terminal not found")
    return {"message": "Terminal deleted successfully"}

@router.post("/{terminal_id}/sync", response_model=TerminalResponse)
def sync_terminal(terminal_id: int, db: Session = Depends(get_db)):
    terminal = TerminalService.sync_terminal(db, terminal_id)
    if not terminal:
        raise HTTPException(status_code=404, detail="Terminal not found")
    return terminal

