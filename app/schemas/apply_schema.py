from app.database.db import Base 
from pydantic import BaseModel, Field
from typing import Optional, List 
from datetime import datetime
from app.models.apply_job import ApplyJob
from app.models.job_model import JobPosting


class ApplyJobCreate(BaseModel):
    job_id: int = Field(..., description="ID of the job being applied for")

class ApplyJobResponse(BaseModel):
    application_id: int
    user_id: int
    job_id: int
    resume_id: Optional[int] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CandidateInfo(BaseModel):
    user_id: int 
    name: str 
    email: str 
    username: str 

class JobInfo(BaseModel):
    job_id: int 
    job_title: str 
    company_name: str 
    location: str
    job_type: str

class ResumeInfo(BaseModel):
    resume_id: int 
    name: str 
    email: str 
    phone: Optional[str]
    skills: Optional[List[str]]
    experience_years: Optional[int]
    education: Optional[str]


    class Config:
        from_attributes = True


class ApplicationDetailResponse(BaseModel):
    application_id: int 
    user_id : int 
    job_id: int 
    resume_id: Optional[int] = None 
    status: str 
    created_at: datetime
    updated_at: datetime 
    candidate_info: CandidateInfo
    job_info: JobInfo
    resume_info: Optional[ResumeInfo] = None
    



