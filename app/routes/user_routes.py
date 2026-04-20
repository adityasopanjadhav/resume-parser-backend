from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.user_schemas import UserSchema, UserLoginSchema, UserResponseSchema, UserLoginResponseSchema
from app.crud.user_crud import create_user, login_user as login_user_service
from app.core.helpers import is_authenticated

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/register", response_model=UserResponseSchema)
def register_user(user : UserSchema, db : Session = Depends(get_db)):
    return create_user(user,db)

@user_router.post("/login", response_model=UserLoginResponseSchema)
def login_user(user : UserLoginSchema, db : Session = Depends(get_db)):
    return login_user_service(user, db)


