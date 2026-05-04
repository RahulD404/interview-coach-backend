from app.modules.video.video_service import process_video


def process_video_pipeline(video_path):
    output = process_video(video_path)

    return {
        "raw": output.get("raw_features", {}),
        "semantic": output.get("semantic_analysis", {})
    }