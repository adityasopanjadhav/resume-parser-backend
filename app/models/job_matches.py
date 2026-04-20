from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String,ForeignKey, Boolean, Float, Text, DateTime
from datetime import datetime 
from app.database.db import Base
import uuid 
import json 

class JobMatch(Base):
    __tablename__ = "job_matches"

    match_id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(String, ForeignKey("resumes.resume_id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_postings.job_id", ondelete="CASCADE"), nullable=False)

    semantic_score = Column(Float, nullable=False)
    ats_score = Column(Float, nullable=False)
    overall_score = Column(Float, nullable=False)

    matched_skils = Column(Text)
    missing_skills = Column(Text)
    expericence_gap = Column(String, nullable=False)
    education_match = Column(Boolean, nullable=False)

    is_saved = Column(Boolean, default=False)
    is_applied = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    