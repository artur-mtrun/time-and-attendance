from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..services.scheduler import SchedulerService
from ..scheduler import scheduler
from pydantic import BaseModel
#from ..models.job import JobInfo, JobUpdate
from ..dependencies.auth import oauth2_scheme

router = APIRouter(tags=["scheduler"])

def get_scheduler_service():
    return SchedulerService(scheduler)

class JobInfo(BaseModel):
    id: str
    name: str
    next_run_time: str | None
    interval: int
    enabled: bool

class JobUpdate(BaseModel):
    interval: int
    enabled: bool

@router.get("/jobs", response_model=List[JobInfo])
async def get_jobs(service: SchedulerService = Depends(get_scheduler_service)):
    return service.get_jobs()

@router.put("/jobs/{job_id}")
async def update_job(
    job_id: str, 
    job_update: JobUpdate,
    service: SchedulerService = Depends(get_scheduler_service)
):
    if not service.update_job(job_id, job_update.interval, job_update.enabled):
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job updated successfully"}

@router.post("/jobs/{job_id}/run")
async def run_job_now(
    job_id: str,
    service: SchedulerService = Depends(get_scheduler_service)
):
    if not service.run_job_now(job_id):
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job triggered successfully"} 