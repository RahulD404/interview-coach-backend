from .extractor import extract_frames, detect_landmarks
from .features import (
    compute_face_presence,
    compute_head_movement,
    compute_gaze_proxy,
    map_video_to_semantics
)
from .semantic_mapper import map_to_semantics


def process_video(video_path):
    frames = extract_frames(video_path)
    landmarks_list = [detect_landmarks(f) for f in frames]

    face_presence = compute_face_presence(landmarks_list)
    head_movement = compute_head_movement(landmarks_list)
    gaze = compute_gaze_proxy(landmarks_list)

    raw_metrics = {
        "face_presence": face_presence,
        "head_movement": head_movement,
        "gaze": gaze
    }

    semantic = map_video_to_semantics(
        face_presence,
        head_movement,
        gaze
    )

    return {
        "raw_features": raw_metrics,
        "semantic_analysis": semantic
    }