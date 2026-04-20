from sqlalchemy.orm import Session 
from fastapi import HTTPException, applications, status
from app.models.apply_job import ApplyJob
from app.schemas.apply_schema import ApplyJobCreate, ApplyJobResponse
from app.models.job_model import JobPosting
from datetime import datetime

def create_application(db : Session, user_id: int , job_id: int):
    existing_application = db.query(ApplyJob).filter(ApplyJob.user_id == user_id, ApplyJob.job_id == job_id).first()

    if existing_application:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already applied for this job.")
    
    new_application = ApplyJob(
        user_id = user_id,
        job_id = job_id,
        status = "applied",
        created_at = datetime.now(),
        updated_at = datetime.now()
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application

def get_user_applications(db : Session, user_id: int):
    
    existing_applications = db.query(ApplyJob).filter(
        ApplyJob.user_id == user_id
    ).all()

    if not existing_applications: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No applications found")

    return existing_applications



def get_application_by_id(db: Session, application_id: int, user_id : int):

    application = db.query(ApplyJob).filter(ApplyJob.application_id == application_id, ApplyJob.user_id == user_id).first()

    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found.")

    return application

def delete_application(db: Session, application_id : int, user_id: int):
    
    application = db.query(ApplyJob).filter(
        ApplyJob.application_id == application_id,
        ApplyJob.user_id == user_id
    ).first()

    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found.")
    
    db.delete(application)
    db.commit()


def get_all_applications(db: Session):

    applications = db.query(ApplyJob).all() 

    if not applications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No applications found.")
    
    return applications

def update_application_status(db: Session, application_id : int, new_status: str):

    application = db.query(ApplyJob).filter(ApplyJob.application_id == application_id).first()

    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found.")
    
    valide_status = ["applied", "interviewing", "rejected", "accepted"]

    if new_status not in valide_status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid status. Valid statuses are: {', '.join(valide_status)}")
    
    application.status = new_status
    application.updated_at = datetime.now()
    db.commit()
    db.refresh(application)
    return application  
    
