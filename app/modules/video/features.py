import numpy as np
from deepface import DeepFace


def compute_face_presence(landmarks_list):
    total = len(landmarks_list)
    present = sum(1 for l in landmarks_list if l is not None)
    return present / total if total else 0


def compute_head_movement(landmarks_list):
    points = []

    for lm in landmarks_list:
        if lm:
            nose = lm.landmark[1]
            points.append((nose.x, nose.y))

    if len(points) < 2:
        return 0

    diffs = np.diff(points, axis=0)
    return float(np.var(diffs))


def compute_gaze_proxy(landmarks_list):
    values = []

    for lm in landmarks_list:
        if lm:
            left_eye = lm.landmark[33]
            right_eye = lm.landmark[263]
            values.append(abs(left_eye.x - right_eye.x))

    return float(np.mean(values)) if values else 0


# 🔥 DeepFace emotion aggregation
def compute_emotion_distribution(frames):
    emotions = []

    for frame in frames:
        try:
            result = DeepFace.analyze(
                frame,
                actions=["emotion"],
                enforce_detection=False
            )
            emotions.append(result[0]["dominant_emotion"])
        except:
            continue

    if not emotions:
        return {"dominant": "neutral", "consistency": 0}

    dominant = max(set(emotions), key=emotions.count)
    consistency = emotions.count(dominant) / len(emotions)

    return {
        "dominant": dominant,
        "consistency": consistency
    }