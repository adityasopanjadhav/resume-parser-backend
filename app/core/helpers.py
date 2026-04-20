from app.database.db import get_db
from app.models.user_model import User
from app.models.admin_model import Admin
from app.core.config import settings 
from sqlalchemy.orm import Session
from datetime import datetime,timedelta
import jwt 
from fastapi import HTTPException, status , Depends,Request


def is_authenticated(request: Request, db : Session = Depends(get_db)):

    try: 
        token = request.headers.get("Authorization")

        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token is missing")
        
        token = token.split(" ")[-1]
        
        data = jwt.decode(token, settings.SECRET_KEY,algorithms=[settings.ALGORITHM])

        user_id = data.get("user_id")
        exp_time = data.get("exp_time")
        current_time = datetime.now().timestamp()

        if current_time > exp_time:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        
        user = db.query(User).filter(User.user_id == user_id).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user 
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")


def is_authenticated_admin(request: Request, db : Session = Depends(get_db)):

    try: 
        token = request.headers.get("Authorization")

        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
        
        token = token.split(" ")[-1]
        
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        admin_id = data.get("admin_id")
        exp_time = data.get("exp_time")
        current_time = datetime.now().timestamp()

        if current_time > exp_time:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        
        admin = db.query(Admin).filter(Admin.admin_id == admin_id).first()

        if not admin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin not found")
        return admin 
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    