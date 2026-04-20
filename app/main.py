from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user_routes import user_router
from app.database.db import Base, engine
from app.models.user_model import User  # Import to register model
from app.routes.admin_routes import admin_router
from app.routes.job_routes import job_router
from app.routes.resume_routes import resume_router
from app.services.job_embeddings import JobEmbeddings
from app.routes.application_routes import application_router
app = FastAPI()

# Create database tables on startup
Base.metadata.create_all(bind=engine)

app.add_middleware(
	CORSMiddleware,
	allow_origins=[
		"http://localhost:3000",
		"http://127.0.0.1:3000",
		"https://resume-parser-frontend-neon.vercel.app/"
	],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(admin_router)
app.include_router(job_router)
app.include_router(resume_router)
app.include_router(application_router)
