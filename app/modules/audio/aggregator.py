# app/modules/audio/aggregator.py


class AudioAggregator:
    def __init__(self):
        pass

    def build_output(self, extractor_data, timing_data, prosody_data, emotion_data):
        """
        Combine all module outputs into final JSON
        """

        return {
            "transcript": extractor_data.get("transcript", ""),
            "fluency": {
                "word_count": timing_data.get("word_count"),
                "speech_rate_wpm": timing_data.get("speech_rate_wpm"),
                "pause_ratio": timing_data.get("pause_ratio"),
                "avg_pause_duration": timing_data.get("avg_pause_duration"),
                "total_pause_time": timing_data.get("total_pause_time"),
            },
            "prosody": {
                "pitch_mean": prosody_data.get("pitch_mean"),
                "pitch_variance": prosody_data.get("pitch_variance"),
                "energy_mean": prosody_data.get("energy_mean"),
                "energy_variance": prosody_data.get("energy_variance"),
            },
            "emotion": {
                "dominant_emotion": emotion_data.get("dominant_emotion"),
                "emotion_variance": emotion_data.get("emotion_variance"),
                "emotion_scores": emotion_data.get("emotion_scores"),
            },
            "metadata": {
                "audio_duration": extractor_data.get("audio_duration"),
                "asr_time": extractor_data.get("asr_time"),
            },
        }
