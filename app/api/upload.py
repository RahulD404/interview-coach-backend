from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlalchemy.orm import Session
import os

from app.db.database import get_db
from app.services.interview_service import process_interview

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_video(
    file: UploadFile = File(...),
    question_id: int = Query(...),
    db: Session = Depends(get_db)
):
    print("📥 Upload received:", file.filename)

    video_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(video_path, "wb") as f:
        f.write(await file.read())

    return process_interview(video_path, question_id, db)