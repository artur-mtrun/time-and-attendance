from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .services.sync_service import SyncService
from .database import SessionLocal

# Globalna instancja schedulera
scheduler = BackgroundScheduler()

def sync_job():
    db = SessionLocal()
    try:
        SyncService.sync_attendance_logs(db)
    finally:
        db.close()

def init_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            sync_job,
            trigger=IntervalTrigger(hours=1),
            id='sync_attendance',
            name='Synchronize attendance logs',
            replace_existing=True
        )
        scheduler.start()
    return scheduler

# Eksportuj scheduler
__all__ = ['scheduler', 'init_scheduler'] 