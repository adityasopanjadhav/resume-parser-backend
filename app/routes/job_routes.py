from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Request
from app.models.job_model import JobPosting, JobStatus
from app.schemas.job_schemas import JobResponse,JobSchema
from app.database.db import get_db
from app.core.helpers import is_authenticated_admin
from app.models.admin_model import Admin
from app.crud.jobs_crud import create_job
from app.crud.jobs_crud import get_job_by_id, get_all_jobs, update_job, delete_job

job_router = APIRouter(prefix="/jobs", tags=["jobs"])

@job_router.post("/create", response_model=JobResponse)
def create_job_endpoint(job : JobSchema, db : Session = Depends(get_db), admin : Admin = Depends(is_authenticated_admin)):
    return create_job(job, db, admin)

@job_router.get("/browse")
def browse_all_jobs(db : Session = Depends(get_db)):
    """Public endpoint to browse all active jobs"""
    jobs = db.query(JobPosting).filter(JobPosting.status == JobStatus.ACTIVE).all()
    return jobs

@job_router.get("/all-jobs")
def get_all_jobs_for_user(db : Session = Depends(get_db)):
    """Get all jobs (for authenticated users)"""
    jobs = db.query(JobPosting).all()
    return jobs

@job_router.get("/all")
def get_all_jobs_endpoint(db : Session = Depends(get_db), admin : Admin = Depends(is_authenticated_admin)):
    return get_all_jobs(db, admin)

@job_router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id : int, db : Session = Depends(get_db), admin : Admin = Depends(is_authenticated_admin)):
    return get_job_by_id(job_id, db, admin)

@job_router.put("/{job_id}", response_model=JobResponse)
def update_job_endpoint(job_id : int, job_data : JobSchema, db : Session = Depends(get_db), admin : Admin = Depends(is_authenticated_admin)):
    return update_job(job_id, job_data, db, admin)

@job_router.delete("/{job_id}")
def delete_job_endpoint(job_id : int, db : Session = Depends(get_db), admin : Admin = Depends(is_authenticated_admin)):
    return delete_job(job_id, db, admin)

