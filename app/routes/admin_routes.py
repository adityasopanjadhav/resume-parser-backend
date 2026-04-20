from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session 
from app.database.db import get_db
from app.schemas.admin_schemas import AdminSchema, AdminLoginSchema, AdminResponseSchema
from app.crud.admin_crud import create_admin, login_admin
from app.core.helpers import is_authenticated
from app.schemas.apply_schema import ApplicationDetailResponse
from app.crud.job_application import get_all_applications, update_application_status
from app.models.apply_job import ApplyJob
from app.models.job_model import JobPosting 
from app.models.user_model import User 
from app.models.resume_model import Resume 
from app.core.helpers import is_authenticated_admin


admin_router = APIRouter(prefix="/admin", tags=["admin"])

@admin_router.post("/register", response_model=AdminResponseSchema)
def register_admin(admin : AdminSchema, db: Session = Depends(get_db)):
    return create_admin(admin, db)

@admin_router.post("/login")
def login_admin_route(admin : AdminLoginSchema , db: Session = Depends(get_db)):
    return login_admin(admin, db)


@admin_router.get("/applications", response_model=list[ApplicationDetailResponse])
def get_all_applications_routes(db: Session = Depends(get_db), admin_id: int = Depends(is_authenticated_admin)):

    applications = db.query(ApplyJob).all() 

    if not applications:
        return [] 
    
    result = [] 

    for app in applications:
        job = db.query(JobPosting).filter(JobPosting.job_id == app.job_id).first()
        candidate = db.query(User).filter(User.user_id == app.user_id).first() 
        resume =db.query(Resume).filter(Resume.resume_id == app.resume_id).first() 

        application_detail = {
            "application_id": app.application_id,
            "user_id": app.user_id,
            "job_id": app.job_id,
            "resume_id": app.resume_id,
            "status": app.status,
            "created_at": app.created_at,
            "updated_at": app.updated_at,
            "candidate_info":{
                "user_id": candidate.user_id,
                "name": candidate.name,
                "email": candidate.email,
                "username": candidate.username
            } if candidate else None,
            "job_info": {
                "job_id": job.job_id,
                "job_title": job.job_title,
                "company_name": job.company_name,
                "location": job.location,
                "job_type": job.job_type
            } if job else None,
            "resume_info": {
                "resume_id" : resume.resume_id,
                "name": resume.name,
                "email": resume.email,
                "phone": resume.phone,
                "skills": resume.skills,
                "experience_years": resume.experience_years,
                "education": resume.education
            } if resume else None
        }

        result.append(application_detail)

    return result 


@admin_router.put("/applications/{application_id}/status")
def update_application_status_endpoint(application_id: int, new_status: str, db: Session = Depends(get_db), admin_id = Depends(is_authenticated_admin)):
    return update_application_status(db, application_id, new_status)


