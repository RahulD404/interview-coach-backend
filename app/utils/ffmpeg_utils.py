import subprocess
import os


FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"

def extract_audio(video_path, output_audio_path):
    command = [
        FFMPEG_PATH,
        "-y",  # ✅ overwrite without asking
        "-i", video_path,
        "-vn",                 # no video
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        output_audio_path
    ]

    print("🚀 Running FFmpeg (audio):", " ".join(command))

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    print("📤 FFMPEG STDOUT:", result.stdout[:200])
    print("⚠️ FFMPEG STDERR:", result.stderr[:500])

    if result.returncode != 0:
        raise Exception(f"FFmpeg failed with error:\n{result.stderr}")

    if not os.path.exists(output_audio_path):
        raise Exception("Audio file was not created!")

    print("✅ Audio extraction complete:", output_audio_path)


def extract_video(video_path, output_video_path):
    command = [
        FFMPEG_PATH,
        "-y",  # ✅ overwrite
        "-i", video_path,
        "-an",  # no audio
        output_video_path
    ]

    print("🚀 Running FFmpeg (video):", " ".join(command))

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    print("📤 FFMPEG STDOUT:", result.stdout[:200])
    print("⚠️ FFMPEG STDERR:", result.stderr[:500])

    if result.returncode != 0:
        raise Exception(f"FFmpeg failed with error:\n{result.stderr}")

    if not os.path.exists(output_video_path):
        raise Exception("Video file was not created!")

    print("✅ Video extraction complete:", output_video_path)