from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserSchema(BaseModel):
    username : str 
    name : str 
    email : EmailStr
    password : str 

class UserLoginSchema(BaseModel):
    username : Optional[str] = None
    email : Optional[EmailStr] = None
    password : str

class UserLoginResponseSchema(BaseModel):
    detail: str
    access_token: str

class UserResponseSchema(BaseModel):
    user_id : int 
    username : str 
    name : str 
    email : EmailStr

    model_config = ConfigDict(from_attributes=True)
    