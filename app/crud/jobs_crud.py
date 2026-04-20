from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Request
from app.models.job_model import JobPosting, JobStatus
from app.schemas.job_schemas import JobResponse, JobSchema
from app.services.job_embeddings import JobEmbeddings
from app.database.db import get_db
from app.core.helpers import is_authenticated
from app.models.admin_model import Admin
from datetime import datetime


def create_job(job : JobSchema, db : Session, admin : Admin):

    existing_job = db.query(JobPosting).filter(JobPosting.job_title == job.job_title, JobPosting.admin_id == admin.admin_id).first()

    if existing_job:
        raise HTTPException(status_code=400, detail="Job with this title already exists")

    new_job = JobPosting(
        job_title = job.job_title,
        company_name = job.company_name,
        location = job.location,
        description = job.description,
        required_skills = job.required_skills,
        experience_years = job.experience_years,
        salary_range = job.salary_range,
        job_type = job.job_type,
        status = JobStatus(job.status.value),
        posted_at = job.posted_at or datetime.now(),
        admin_id = admin.admin_id
    )    

    db.add(new_job)
    db.commit()
    db.refresh(new_job)



    try:
        job_embeddings = JobEmbeddings()
        job_embeddings.sync_add_job(new_job)
    except Exception as e:
        print(f"Error syncing job embeddings: {e}")

    return new_job

def get_job_by_id(job_id : int, db : Session, admin : Admin):

    job = db.query(JobPosting).filter(JobPosting.job_id == job_id, JobPosting.admin_id == admin.admin_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job


def get_all_jobs(db : Session, admin : Admin):

    jobs = db.query(JobPosting).filter(JobPosting.admin_id == admin.admin_id).all()

    return jobs


def update_job(job_id : int, job_data : JobSchema, db : Session, admin : Admin):

    job = db.query(JobPosting).filter(JobPosting.job_id == job_id, JobPosting.admin_id == admin.admin_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job.job_title = job_data.job_title
    job.company_name = job_data.company_name
    job.location = job_data.location
    job.description = job_data.description
    job.required_skills = job_data.required_skills
    job.experience_years = job_data.experience_years
    job.salary_range = job_data.salary_range
    job.job_type = job_data.job_type
    job.status = JobStatus(job_data.status.value)

    db.commit() 
    db.refresh(job)

    try:
        job_embeddings = JobEmbeddings()
        job_embeddings.sync_update_job(job)
    except Exception as e:
        print(f"Error syncing job embeddings: {e}")
        
    return job


def delete_job(job_id : int, db: Session, admin : Admin):

    job = db.query(JobPosting).filter(JobPosting.job_id == job_id, JobPosting.admin_id == admin.admin_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db.delete(job)
    db.commit()

    try:
        job_embeddings = JobEmbeddings()
        job_embeddings.sync_delete_job(job_id)
    except Exception as e:
        print(f"Error syncing job embeddings: {e}")

    return {"detail" : "Job deleted successfully"}