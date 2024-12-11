from apscheduler.schedulers.background import BackgroundScheduler
from typing import List, Dict, Any
from datetime import datetime

class SchedulerService:
    def __init__(self, scheduler: BackgroundScheduler):
        self.scheduler = scheduler

    def get_jobs(self) -> List[Dict[str, Any]]:
        jobs = self.scheduler.get_jobs()
        return [
            {
                "id": job.id,
                "name": job.name,
                "next_run_time": str(job.next_run_time) if job.next_run_time else None,
                "interval": int(job.trigger.interval.total_seconds() // 60),
                "enabled": job.next_run_time is not None
            }
            for job in jobs
        ]

    def update_job(self, job_id: str, interval: int, enabled: bool) -> bool:
        job = self.scheduler.get_job(job_id)
        if not job:
            return False
        
        if enabled:
            self.scheduler.resume_job(job_id)
            self.scheduler.modify_job(
                job_id,
                trigger='interval',
                minutes=interval
            )
        else:
            self.scheduler.pause_job(job_id)
        return True

    def run_job_now(self, job_id: str) -> bool:
        job = self.scheduler.get_job(job_id)
        if not job:
            return False
        
        job.func()
        return True 