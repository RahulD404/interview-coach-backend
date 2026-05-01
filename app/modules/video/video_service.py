from .extractor import extract_frames, detect_landmarks
from .features import (
    compute_face_presence,
    compute_head_movement,
    compute_gaze_proxy,
    compute_emotion_distribution
)
from .semantic_mapper import map_to_semantics


def process_video(video_path):
    frames = extract_frames(video_path)

    landmarks_list = [
        detect_landmarks(frame) for frame in frames
    ]

    features = {
        "face_presence": compute_face_presence(landmarks_list),
        "head_movement": compute_head_movement(landmarks_list),
        "gaze": compute_gaze_proxy(landmarks_list),
        "emotion": compute_emotion_distribution(frames)
    }

    semantics = map_to_semantics(features)

    return {
        "raw_features": features,
        "semantic_analysis": semantics
    }