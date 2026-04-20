from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
import datetime
from enum import Enum


class JobStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DRAFT  = "draft"


class JobSchema(BaseModel):
    job_id: Optional[int] = None
    job_title: str
    company_name: str
    location: str
    description: str
    required_skills: List[str]
    experience_years: int
    salary_range: Optional[str] = None
    job_type: str
    status: JobStatusEnum = JobStatusEnum.DRAFT
    posted_at: Optional[datetime.datetime] = None


class JobResponse(BaseModel):
    job_id: int
    job_title: str
    company_name: str
    location: str
    description: str
    required_skills: List[str]
    experience_years: int
    salary_range: Optional[str] = None
    job_type: str
    status: JobStatusEnum
    
    model_config = ConfigDict(from_attributes=True)
    posted_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
