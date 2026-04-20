from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Request, Depends
from app.models.admin_model import Admin
from app.schemas.admin_schemas import AdminSchema,AdminLoginSchema
from app.database.db import get_db
from pwdlib import PasswordHash
from datetime import datetime, timedelta
from app.core.config import settings
import time
import jwt 

password_hasher = PasswordHash.recommended()


def get_password_hash(password : str)-> str:
    return password_hasher.hash(password)

def verify_password(plain_password : str, hashed_password : str) -> bool:
    return password_hasher.verify(plain_password, hashed_password)

def create_admin(admin : AdminSchema, db : Session):
    existing_admin = db.query(Admin).filter(Admin.admin_email == admin.admin_email).first()

    if existing_admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin with this email already exists")
    
    hashed_password = get_password_hash(admin.password)

    new_admin = Admin(
        admin_name = admin.admin_name,
        admin_email = admin.admin_email,
        hashed_password = hashed_password
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin

def login_admin(admin : AdminLoginSchema, db : Session):
    existing_admin = db.query(Admin).filter(Admin.admin_email == admin.admin_email).first()

    if existing_admin is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    
    if not verify_password(admin.password, existing_admin.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    exp_time = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    token = jwt.encode({"admin_id" : existing_admin.admin_id, "exp_time" : exp_time.timestamp()}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return {"detail" : "Login successful", "access_token" : token}



