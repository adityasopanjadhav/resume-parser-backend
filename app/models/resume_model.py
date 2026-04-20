from sqlalchemy.orm import Session 
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime,Float
from datetime import datetime

from tomlkit import string
from app.database.db import Base
import uuid

class Resume(Base):
    __tablename__ = "resumes"

    resume_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)

    # parsed data fields 

    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    skills = Column(Text, nullable=True)
    experience_years = Column(Float, nullable=True)
    education_level = Column(Text, nullable=True)

    # MetaDATA  

    parsed_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    
    