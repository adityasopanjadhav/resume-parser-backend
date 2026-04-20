from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class AdminSchema(BaseModel):
    admin_name: str
    admin_email: EmailStr
    password: str
    id: Optional[int] = None


class AdminResponseSchema(BaseModel):
    admin_id: int
    admin_name: str
    admin_email: EmailStr
    
    model_config = ConfigDict(from_attributes=True)


class AdminLoginSchema(BaseModel):
    admin_email: EmailStr
    password: str   