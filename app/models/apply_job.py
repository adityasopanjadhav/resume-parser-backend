from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Session, relationship
from app.database.db import Base
from datetime import datetime
import uuid 


class ApplyJob(Base):
    __tablename__ = "apply_jobs"

    application_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_postings.job_id", ondelete="CASCADE"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id", ondelete="SET NULL"), nullable=True)

    status = Column(String(50), default="applied")  # e.g., "applied", "interviewing", "rejected", "accepted"
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)




