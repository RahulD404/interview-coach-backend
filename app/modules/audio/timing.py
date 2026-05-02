# app/modules/audio/timing.py

import numpy as np


class TimingAnalyzer:
    def __init__(self):
        pass

    def extract_word_timings(self, segments):
        """
        Extract all word-level timestamps into a flat list.
        """
        word_timings = []

        for seg in segments:
            for word in seg.get("words", []):
                start = word.get("start")
                end = word.get("end")

                if start is not None and end is not None:
                    word_timings.append((start, end))

        return word_timings

    def compute_pause_metrics(self, word_timings):
        """
        Compute pause durations between consecutive words.
        """
        pauses = []

        for i in range(len(word_timings) - 1):
            current_end = word_timings[i][1]
            next_start = word_timings[i + 1][0]

            gap = next_start - current_end

            if gap > 0:  # ignore negative/overlap
                pauses.append(gap)

        total_pause_time = sum(pauses)

        avg_pause_duration = total_pause_time / len(pauses) if pauses else 0.0

        return pauses, total_pause_time, avg_pause_duration

    def compute_speech_metrics(self, word_timings, total_duration):
        """
        Compute speech-related metrics.
        """
        word_count = len(word_timings)

        # Total speech time = sum of word durations
        speech_time = sum(end - start for start, end in word_timings)

        # Words per minute
        speech_rate_wpm = (
            (word_count / total_duration) * 60 if total_duration > 0 else 0
        )

        return word_count, speech_time, speech_rate_wpm

    def compute_pause_ratio(self, total_pause_time, total_duration):
        """
        Ratio of silence vs total duration.
        """
        return total_pause_time / total_duration if total_duration > 0 else 0

    def analyze(self, segments, total_duration):
        """
        Main function to compute all timing metrics.
        """
        word_timings = self.extract_word_timings(segments)

        if not word_timings:
            return {}

        pauses, total_pause_time, avg_pause_duration = self.compute_pause_metrics(
            word_timings
        )

        word_count, speech_time, speech_rate_wpm = self.compute_speech_metrics(
            word_timings, total_duration
        )

        pause_ratio = self.compute_pause_ratio(total_pause_time, total_duration)

        return {
            "word_count": word_count,
            "speech_rate_wpm": round(speech_rate_wpm, 2),
            "total_pause_time": round(total_pause_time, 2),
            "avg_pause_duration": round(avg_pause_duration, 2),
            "pause_ratio": round(pause_ratio, 3),
            "total_speech_time": round(speech_time, 2),
        }
