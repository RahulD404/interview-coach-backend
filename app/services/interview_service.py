from app.modules.audio.pipeline import process_audio
from app.modules.video.pipeline import process_video_pipeline
from app.services.llm_service import evaluate_answer
from app.db.models import Session as DBSession, Response, Question


def process_interview(video_path, question_id, db):
    print("\n🚀 INTERVIEW SERVICE START")

    # ---------------- AUDIO ----------------
    audio = process_audio(video_path)
    print("✅ Audio pipeline done")

    # ---------------- VIDEO ----------------
    video = process_video_pipeline(video_path)
    print("✅ Video pipeline done")

    # ---------------- QUESTION ----------------
    question_obj = db.query(Question).filter(Question.id == question_id).first()
    if not question_obj:
        raise Exception("Invalid question_id")

    # ---------------- LLM ----------------
    result = evaluate_answer(
        question_obj.question,
        audio["transcript"],
        question_obj.expected_answer,
        audio["semantic"],
        video["semantic"]
    )

    print("✅ LLM evaluation done")

    # ---------------- DB ----------------
    session = DBSession()
    db.add(session)
    db.commit()
    db.refresh(session)

    response = Response(
        session_id=session.id,
        question_id=question_id,
        question=question_obj.question,
        transcript=audio["transcript"],
        audio_metrics=audio["raw"],
        video_metrics=video["raw"],
        evaluation=result.get("evaluation", {})
    )

    db.add(response)
    db.commit()

    print("✅ DB stored")
    print("🎯 INTERVIEW SERVICE END\n")

    return {
        "session_id": session.id,
        "question": question_obj.question,
        "transcript": audio["transcript"],
        "audio_analysis": audio["semantic"],
        "video_analysis": video["semantic"],
        "evaluation": result.get("evaluation", {})
    }