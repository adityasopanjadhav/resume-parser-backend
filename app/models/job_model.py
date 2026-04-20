from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, Boolean, Enum,ForeignKey
from app.database.db import Base
import enum


class JobStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DRAFT = "draft"


class JobPosting(Base):
    __tablename__ = "job_postings"

    job_id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    required_skills = Column(JSON, nullable=False)
    experience_years = Column(Integer, nullable=False)
    salary_range = Column(String(50), nullable=True)
    job_type = Column(String(50), nullable=False) 
    status = Column(Enum(JobStatus), default=JobStatus.DRAFT, nullable=False)
    posted_at = Column(DateTime, nullable=False)


    admin_id = Column(Integer, ForeignKey("admins.admin_id", ondelete="CASCADE"), nullable=False)

