import time
import json
import re
from pydantic import BaseModel, ValidationError

from app.modules.llm.model import generate_response
from app.modules.llm.prompt_builder import build_prompt


# ================================
# ✅ SCHEMA (STRICT VALIDATION)
# ================================
class Evaluation(BaseModel):
    content_score: int
    structure_score: int
    communication_score: int
    confidence_score: int
    overall_score: int
    strengths: list[str]
    weaknesses: list[str]
    improvements: list[str]
    detailed_feedback: str


# ================================
# ✅ ROBUST JSON EXTRACTION
# ================================
def extract_json(text: str):
    """
    Extract first valid JSON object from messy LLM output.
    Handles:
    - extra braces (} })
    - markdown
    - extra text before/after
    """
    matches = re.findall(r"\{.*?\}", text, re.DOTALL)

    for match in matches:
        try:
            return json.loads(match)
        except:
            continue

    return None


# ================================
# ✅ SCORE CALIBRATION (HYBRID)
# ================================
def adjust_scores(data, audio_metrics, video_metrics):
    filler = audio_metrics.get("filler_words", 0)
    pauses = audio_metrics.get("pause_count", 0)

    # Penalize communication issues
    if filler > 2:
        data["communication_score"] = max(0, data["communication_score"] - 2)

    if pauses > 3:
        data["communication_score"] = max(0, data["communication_score"] - 1)

    # Recompute overall score (deterministic)
    data["overall_score"] = round(
        0.4 * data["content_score"] +
        0.2 * data["structure_score"] +
        0.2 * data["communication_score"] +
        0.2 * data["confidence_score"]
    )

    return data


# ================================
# 🚀 MAIN PIPELINE
# ================================
def evaluate_answer(
    question,
    transcript,
    expected_answer,
    audio_metrics=None,
    video_metrics=None
):
    start = time.time()

    prompt = build_prompt(
        question,
        transcript,
        expected_answer,
        audio_metrics,
        video_metrics
    )

    raw_output = generate_response(prompt)

    parsed = extract_json(raw_output)

    # ❌ Parsing failed
    if parsed is None:
        return {
            "latency_seconds": round(time.time() - start, 2),
            "error": "Parsing failed",
            "raw_output": raw_output
        }

    # ❌ Schema validation failed
    try:
        validated = Evaluation(**parsed).dict()
    except ValidationError:
        return {
            "latency_seconds": round(time.time() - start, 2),
            "error": "Schema validation failed",
            "parsed": parsed
        }

    # ✅ Apply deterministic corrections
    final = adjust_scores(validated, audio_metrics or {}, video_metrics or {})

    return {
        "latency_seconds": round(time.time() - start, 2),
        "evaluation": final
    }