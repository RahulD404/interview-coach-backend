# app/modules/audio/config.py

import os
from dotenv import load_dotenv
import torch

# Load environment variables
load_dotenv()

# ========================
# DEVICE CONFIG
# ========================

DEVICE = os.getenv("DEVICE", "cpu")

if DEVICE == "cuda" and not torch.cuda.is_available():
    DEVICE = "cpu"

FFMPEG_PATH = r"C:\Users\Rahul\Downloads\ffmpeg-2026-04-30-git-cc3ca17127-essentials_build\ffmpeg-2026-04-30-git-cc3ca17127-essentials_build\bin"
# ========================
# MODEL CONFIG
# ========================

WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL", "base")

EMOTION_MODEL_NAME = "superb/wav2vec2-large-superb-er"

WAV2VEC_MODEL_NAME = "facebook/wav2vec2-base"

# ========================
# AUDIO CONFIG
# ========================

TARGET_SAMPLE_RATE = 16000

# ========================
# PATH CONFIG
# ========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_AUDIO_DIR = os.path.join(DATA_DIR, "raw_audio")
TRANSCRIPTS_DIR = os.path.join(DATA_DIR, "transcripts")

# ========================
# PERFORMANCE CONFIG
# ========================

ENABLE_TIMING_LOGS = True