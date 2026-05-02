# app/modules/audio/emotion.py

import torch
import numpy as np
from transformers import AutoModelForAudioClassification, AutoFeatureExtractor
import logging

logging.getLogger("transformers").setLevel(logging.ERROR)


class EmotionAnalyzer:
    def __init__(self):
        self.model_name = "superb/wav2vec2-large-superb-er"

        self.feature_extractor = AutoFeatureExtractor.from_pretrained(self.model_name)
        self.model = AutoModelForAudioClassification.from_pretrained(self.model_name)

        self.model.eval()

    def analyze(self, audio, sr):
        """
        Analyze emotion from audio
        """

        # Convert to model input
        inputs = self.feature_extractor(
            audio, sampling_rate=sr, return_tensors="pt", padding=True
        )

        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits
        probs = torch.nn.functional.softmax(logits, dim=-1).numpy()[0]

        labels = self.model.config.id2label

        LABEL_MAP = {
            "hap": "happy",
            "neu": "neutral",
            "ang": "angry",
            "sad": "sad",
            "fea": "fear",
        }

        emotion_scores = {
            LABEL_MAP.get(labels[i], labels[i]): float(probs[i])
            for i in range(len(probs))
        }
        # Dominant emotion
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)

        # Variance (stability)
        emotion_variance = float(np.var(list(emotion_scores.values())))

        return {
            "emotion_scores": emotion_scores,
            "dominant_emotion": dominant_emotion,
            "emotion_variance": round(emotion_variance, 4),
        }
