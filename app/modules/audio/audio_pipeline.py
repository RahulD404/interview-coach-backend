# app/services/audio_pipeline.py

from app.modules.audio.extractor import AudioExtractor
from app.modules.audio.timing import TimingAnalyzer
from app.modules.audio.prosody import ProsodyAnalyzer
from app.modules.audio.emotion import EmotionAnalyzer
from app.modules.audio.aggregator import AudioAggregator


class AudioPipeline:
    def __init__(self):
        self.extractor = AudioExtractor()
        self.timing = TimingAnalyzer()
        self.prosody = ProsodyAnalyzer()
        self.emotion = EmotionAnalyzer()
        self.aggregator = AudioAggregator()

    def process(self, video_path):
        # Step 1: Extract
        result = self.extractor.transcribe(video_path)

        # Step 2: Timing
        timing_metrics = self.timing.analyze(
            result["segments"], result["audio_duration"]
        )

        # Step 3: Prosody
        prosody_metrics = self.prosody.analyze(
            result["audio_array"], result["sample_rate"]
        )

        # Step 4: Emotion
        emotion_metrics = self.emotion.analyze(
            result["audio_array"], result["sample_rate"]
        )

        # Step 5: Aggregate
        final_output = self.aggregator.build_output(
            result, timing_metrics, prosody_metrics, emotion_metrics
        )

        return final_output
