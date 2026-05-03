def map_audio_to_semantics(audio_raw):
    fluency = audio_raw.get("fluency", {})
    prosody = audio_raw.get("prosody", {})
    emotion = audio_raw.get("emotion", {})

    speech_rate = fluency.get("speech_rate_wpm", 0)
    pause_ratio = fluency.get("pause_ratio", 0)

    pitch_var = prosody.get("pitch_variance", 0)
    energy_var = prosody.get("energy_variance", 0)

    dominant_emotion = emotion.get("dominant_emotion", "neutral")

    return {
        "speech_fluency": describe_fluency(pause_ratio),
        "speaking_pace": describe_speech_rate(speech_rate),
        "voice_modulation": describe_pitch(pitch_var),
        "energy_level": describe_energy(energy_var),
        "emotional_tone": dominant_emotion
    }


def describe_fluency(pause_ratio):
    if pause_ratio < 0.1:
        return "smooth and fluent"
    elif pause_ratio < 0.3:
        return "moderate with some pauses"
    else:
        return "frequent pauses affecting fluency"


def describe_speech_rate(rate):
    if rate < 110:
        return "slow"
    elif rate < 160:
        return "moderate"
    else:
        return "fast"


def describe_pitch(pitch_var):
    if pitch_var < 0.01:
        return "monotone"
    elif pitch_var < 0.05:
        return "moderate variation"
    else:
        return "highly expressive"


def describe_energy(energy_var):
    if energy_var < 0.01:
        return "flat energy"
    elif energy_var < 0.05:
        return "stable energy"
    else:
        return "dynamic energy"