print("🔥 Upload endpoint hit")
from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlalchemy.orm import Session
import shutil, os

from app.db.database import get_db
from app.db.models import Session as DBSession, Response, Question

from app.utils.ffmpeg_utils import extract_audio
from app.modules.video.video_service import process_video

from app.modules.audio.audio_service import AudioService
from app.modules.audio.semantic_mapper import map_audio_to_semantics

from app.services.llm_service import evaluate_answer

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

audio_service = AudioService()


@router.post("/upload")
async def upload_video(
    file: UploadFile = File(...),
    question_id: int = Query(...), 
    db: Session = Depends(get_db)
):
    print("🔥 STEP 1: endpoint hit")
    # -----------------------------
    # 1. Save uploaded video
    # -----------------------------
    video_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # -----------------------------
    # 2. Extract audio (FFmpeg)
    # -----------------------------
    audio_path = video_path.replace(".mp4", ".wav")
    extract_audio(video_path, audio_path)

    # -----------------------------
    # 3. AUDIO PROCESSING (FULL)
    # -----------------------------
    audio_raw = audio_service.process(video_path)

    audio_metrics_db = audio_raw  # full storage
    audio_semantics = map_audio_to_semantics(audio_raw)

    transcript = audio_raw.get("transcript", "")

    # -----------------------------
    # 4. VIDEO PROCESSING
    # -----------------------------
    video_output = process_video(video_path)

    video_metrics_db = video_output.get("raw_features", {})
    video_semantics = video_output.get("semantic_analysis", {})

    # -----------------------------
    # 5. FETCH QUESTION FROM DB
    # -----------------------------
    question_obj = db.query(Question).filter(Question.id == question_id).first()

    if not question_obj:
        return {"error": "Invalid question_id"}

    question = question_obj.question
    expected = question_obj.expected_answer

    # -----------------------------
    # 6. LLM EVALUATION
    # -----------------------------
    result = evaluate_answer(
        question,
        transcript,
        expected,
        audio_semantics,
        video_semantics
    )

    # -----------------------------
    # 7. STORE IN DB
    # -----------------------------
    session = DBSession()
    db.add(session)
    db.commit()
    db.refresh(session)

    response = Response(
        session_id=session.id,
        question_id=question_id,   # 👈 NEW (important)
        question=question,
        transcript=transcript,

        audio_metrics=audio_metrics_db,
        video_metrics=video_metrics_db,

        evaluation=result.get("evaluation", {})
    )

    db.add(response)
    db.commit()

    # -----------------------------
    # 8. RESPONSE
    # -----------------------------
    return {
        "session_id": session.id,
        "question": question,
        "transcript": transcript,
        "audio_analysis": audio_semantics,
        "video_analysis": video_semantics,
        "evaluation": result.get("evaluation", {})
    }