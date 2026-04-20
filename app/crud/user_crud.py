from sqlalchemy.orm import Session 
from fastapi import HTTPException, status, Request, Depends
from datetime import datetime, timedelta
from pwdlib import PasswordHash
from app.core.config import settings
import jwt
from app.database.db import get_db
from app.models.user_model import User 
from app.schemas.user_schemas import UserSchema, UserResponseSchema, UserLoginSchema  

password_hasher = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(plain_password, hashed_password)


def create_user(user : UserSchema, db : Session):
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already exists")
    
    hashed_password = get_password_hash(user.password)

    new_user = User(
        username = user.username,
        name = user.name,
        email = user.email,
        hashed_password = hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(user : UserLoginSchema, db : Session):

    if not user.username and not user.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Either username or email is required")

    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()

    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or email")
    
    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    exp_time = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    token = jwt.encode({"user_id" : existing_user.user_id, "exp_time" : exp_time.timestamp()}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return {"detail" : "Login successful", "access_token" : token}


