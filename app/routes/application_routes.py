from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models import job_model
from app.schemas.apply_schema import ApplyJobResponse, ApplyJobCreate
from app.crud.job_application import create_application, get_user_applications, get_application_by_id, delete_application
from app.core.helpers import is_authenticated, is_authenticated_admin

application_router = APIRouter(prefix="/applications", tags=["applications"])


@application_router.post("/apply", response_model=ApplyJobResponse)
def apply_for_job(application : ApplyJobCreate, db : Session = Depends(get_db), user = Depends(is_authenticated)):
    return create_application(db, user.user_id, application.job_id)

@application_router.get("/my-applications", response_model=list[ApplyJobResponse])
def get_my_applications(db : Session = Depends(get_db), user = Depends(is_authenticated)):
    return get_user_applications(db, user.user_id)

@application_router.get("/{application_id}", response_model=ApplyJobResponse)
def get_application_information(application_id : int, db : Session = Depends(get_db), User = Depends(is_authenticated)):
    return get_application_by_id(db, application_id=application_id, user_id=User.user_id)

@application_router.delete("/{application_id}")
def delete_application_route(application_id : int, db : Session = Depends(get_db), user = Depends(is_authenticated)):
    delete_application(db, application_id=application_id, user_id=user.user_id)
    return {"detail": "Application deleted successfully"}

