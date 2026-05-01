from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.utils.ffmpeg_utils import extract_audio
from app.modules.video.video_service import process_video

router = APIRouter()


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    video_path = os.path.join(UPLOAD_DIR, file.filename)

    # save file
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # extract audio
    audio_path = video_path.replace(".mp4", ".wav")
    extract_audio(video_path, audio_path)

    # process video
    video_metrics = process_video(video_path)

    return {
        "audio_path": audio_path,
        "video_analysis": video_metrics
    }