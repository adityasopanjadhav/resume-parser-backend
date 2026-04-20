# app/routes/resume.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import uuid
import os

from app.services.file_parser import extract_text_from_file
from app.services.resume_embeddings import resume_embeddings
from app.services.matching_service import match_jobs_for_resume
from app.core.helpers import is_authenticated

resume_router = APIRouter(prefix="/resume", tags=["resumes"])

UPLOAD_DIR = "./uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@resume_router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user = Depends(is_authenticated)
):
    """
    Upload → Embed → Auto Match → Return Jobs
    """
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
        raise HTTPException(status_code=400, detail="Only PDF/DOCX allowed")

    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        text = extract_text_from_file(file_path)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Extraction failed: {e}")

    if not text.strip():
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="Empty resume")

    user_id = str(current_user.user_id)

    try:
        resume_id = resume_embeddings.add_resume(text, user_id)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Vector DB error: {e}")

    try:
        matches = match_jobs_for_resume(resume_id, top_k=5)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Matching failed: {e}")

    return {
        "resume_id": resume_id,
        "matches": matches
    }