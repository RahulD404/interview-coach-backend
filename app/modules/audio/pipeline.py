from app.modules.audio.audio_pipeline import AudioPipeline
from app.modules.audio.semantic_mapper import map_audio_to_semantics

audio_pipeline = AudioPipeline()


def process_audio(video_path):
    raw = audio_pipeline.process(video_path)

    semantic = map_audio_to_semantics(raw)

    return {
        "transcript": raw.get("transcript", ""),
        "raw": raw,
        "semantic": semantic
    }