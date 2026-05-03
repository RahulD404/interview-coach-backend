import numpy as np


# -----------------------------
# RAW METRICS
# -----------------------------

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


# -----------------------------
# SEMANTIC MAPPING (KEY PART)
# -----------------------------

def map_video_to_semantics(face_presence, head_movement, gaze):
    return {
        "face_visibility": describe_face(face_presence),
        "stability": describe_movement(head_movement),
        "eye_contact": describe_gaze(gaze)
    }


def describe_face(val):
    if val > 0.8:
        return "face consistently visible"
    elif val > 0.5:
        return "face partially visible"
    else:
        return "face often not visible"


def describe_movement(val):
    if val < 0.001:
        return "very stable posture"
    elif val < 0.01:
        return "moderate movement"
    else:
        return "excessive movement"


def describe_gaze(val):
    if val < 0.02:
        return "good eye alignment (likely maintaining eye contact)"
    elif val < 0.05:
        return "moderate eye alignment"
    else:
        return "poor eye alignment (likely looking away frequently)"