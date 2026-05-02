# app/modules/audio/prosody.py

import numpy as np
import librosa


class ProsodyAnalyzer:
    def __init__(self):
        pass

    # def load_audio(self, audio_path):
    #     audio, sr = librosa.load(audio_path, sr=16000)
    #     return audio, sr

    def compute_energy(self, audio):
        """
        RMS energy (loudness)
        """
        energy = librosa.feature.rms(y=audio)[0]
        return np.mean(energy), np.var(energy)

    def compute_pitch(self, audio, sr):
        """
        Better pitch estimation using YIN
        """
        pitches = librosa.yin(audio, fmin=50, fmax=300, sr=sr)

        # Remove invalid values
        pitches = pitches[~np.isnan(pitches)]

        if len(pitches) == 0:
            return 0.0, 0.0

        return np.mean(pitches), np.var(pitches)

    def analyze(self, audio, sr):
        """
        Main function
        """
        # audio, sr = self.load_audio(audio)

        energy_mean, energy_var = self.compute_energy(audio)
        pitch_mean, pitch_var = self.compute_pitch(audio, sr)

        return {
            "energy_mean": round(float(energy_mean), 4),
            "energy_variance": round(float(energy_var), 4),
            "pitch_mean": round(float(pitch_mean), 2),
            "pitch_variance": round(float(pitch_var), 2),
        }
