# app/modules/audio/extractor.py

import os
import time
import json
import uuid
import subprocess
import soundfile as sf
from faster_whisper import WhisperModel

from app.modules.audio.config import (
    DEVICE,
    WHISPER_MODEL_SIZE,
    TARGET_SAMPLE_RATE,
    FFMPEG_PATH,
    RAW_AUDIO_DIR,
    TRANSCRIPTS_DIR,
)


class AudioExtractor:
    def __init__(self):
        print("🔄 Loading Whisper model...")
        self.model = WhisperModel(
            WHISPER_MODEL_SIZE,
            device=DEVICE,
            compute_type="int8" if DEVICE == "cpu" else "float16",
        )
        print("✅ Whisper loaded")

    # =========================
    # 1. INPUT HANDLER
    # =========================

    def process_input(self, input_path: str) -> str:
        if input_path.endswith((".mp4", ".mov", ".mkv")):
            return self._extract_audio(input_path)
        return input_path

    # =========================
    # 2. VIDEO → AUDIO (FIXED)
    # =========================

    def _extract_audio(self, video_path: str) -> str:
        os.makedirs(RAW_AUDIO_DIR, exist_ok=True)

        file_id = str(uuid.uuid4())[:8]
        temp_audio_path = os.path.join(RAW_AUDIO_DIR, f"audio_{file_id}.wav")

        command = [
            FFMPEG_PATH,
            "-y",
            "-i", video_path,
            "-vn",
            "-ac", "1",
            "-ar", str(TARGET_SAMPLE_RATE),
            "-f", "wav",
            temp_audio_path,
        ]

        print("\n🚀 [Extractor] Running FFmpeg:")
        print(" ".join(command))

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        print("📤 FFmpeg STDOUT:", result.stdout[:200])
        print("⚠️ FFmpeg STDERR:", result.stderr[:500])

        if result.returncode != 0:
            raise Exception(f"❌ FFmpeg failed:\n{result.stderr}")

        if not os.path.exists(temp_audio_path):
            raise Exception("❌ Audio file not created")

        print("✅ [Extractor] Audio extracted:", temp_audio_path)

        return temp_audio_path

    # =========================
    # 3. LOAD AUDIO
    # =========================

    def load_audio(self, audio_path: str):
        audio, sr = sf.read(audio_path)

        if len(audio.shape) > 1:
            audio = audio.mean(axis=1)

        return audio, sr

    # =========================
    # 4. ASR
    # =========================

    def transcribe(self, input_path: str):
        print("\n➡️ [Extractor] Starting transcription:", input_path)

        start_time = time.time()
        file_id = str(uuid.uuid4())[:8]

        # Step 1: Normalize input
        audio_path = self.process_input(input_path)

        # Step 2: Load audio
        audio, sr = self.load_audio(audio_path)

        print("➡️ [Extractor] Running Whisper...")

        # Step 3: ASR
        segments, info = self.model.transcribe(
            audio,
            beam_size=5,
            word_timestamps=True
        )

        transcript = ""
        all_segments = []

        for segment in segments:
            segment_data = {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip(),
                "words": [],
            }

            transcript += segment.text

            if segment.words:
                for word in segment.words:
                    segment_data["words"].append({
                        "word": word.word,
                        "start": word.start,
                        "end": word.end
                    })

            all_segments.append(segment_data)

        total_time = round(time.time() - start_time, 2)

        os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

        transcript_file = os.path.join(
            TRANSCRIPTS_DIR,
            f"transcript_{file_id}.json"
        )

        with open(transcript_file, "w", encoding="utf-8") as f:
            json.dump(
                {"transcript": transcript.strip(), "segments": all_segments},
                f,
                indent=2,
            )

        print(f"✅ [Extractor] Done in {total_time}s")

        return {
            "transcript": transcript.strip(),
            "segments": all_segments,
            "audio_duration": info.duration,
            "asr_time": total_time,
            "audio_path": audio_path,
            "audio_array": audio,
            "sample_rate": sr,
        }