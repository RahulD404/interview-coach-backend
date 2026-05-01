def map_to_semantics(features):
    return {
        "eye_contact": describe_eye_contact(features["gaze"]),
        "movement": describe_movement(features["head_movement"]),
        "presence": describe_presence(features["face_presence"]),
        "facial_expression": describe_emotion(
            features["emotion"]["dominant"],
            features["emotion"]["consistency"]
        )
    }


def describe_eye_contact(val):
    if val > 0.7:
        return "stable and strong eye contact"
    elif val > 0.4:
        return "moderate but inconsistent eye contact"
    else:
        return "weak and unstable eye contact"


def describe_movement(val):
    if val < 0.2:
        return "very stable head movement"
    elif val < 0.5:
        return "moderate movement"
    else:
        return "frequent and restless movement"


def describe_presence(val):
    if val > 0.9:
        return "face consistently visible"
    elif val > 0.6:
        return "face mostly visible"
    else:
        return "face frequently missing from frame"


def describe_emotion(dominant, consistency):
    if dominant == "happy" and consistency > 0.6:
        return "engaged and expressive"
    elif dominant == "neutral":
        return "mostly neutral expression"
    else:
        return "low emotional expressiveness"