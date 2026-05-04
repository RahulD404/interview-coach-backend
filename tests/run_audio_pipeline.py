# tests/test_audio_service.py

import os
from app.modules.audio.audio_pipeline import AudioService


def test_audio_service():
    print("\n🔍 Testing Audio Service...\n")

    video_path = os.path.join(
        "app", "modules", "audio", "data", "input_video", "sample.mp4"
    )

    if not os.path.exists(video_path):
        print("❌ Video not found")
        return

    service = AudioService()
    result = service.process(video_path)

    print("Final Output:\n", result)

    # Basic checks
    assert "transcript" in result
    assert "fluency" in result
    assert "prosody" in result
    assert "emotion" in result

    print("\n✅ Audio Service working correctly!\n")


if __name__ == "__main__":
    test_audio_service()
