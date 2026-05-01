from fastapi import APIRouter
from app.services.llm_service import evaluate_answer

router = APIRouter()


@router.get("/llm/test")
def test_llm():
    question = "Tell me about yourself"

    transcript = """
    Hi, I am Rahul. I recently graduated in computer science.
    I like coding and solving problems. I have worked on a few projects
    including web apps and machine learning basics.
    """

    expected = "Should include background, skills, experience, and career goals."

    audio_metrics = {
        "speech_rate": 140,
        "filler_words": 3,
        "pause_count": 5
    }

    video_metrics = {
        "eye_contact": 0.7,
        "confidence_score": 0.65
    }

    return evaluate_answer(
        question,
        transcript,
        expected,
        audio_metrics,
        video_metrics
    )