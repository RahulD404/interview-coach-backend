from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Question

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get("")
def get_questions(
    role: str = Query(...),
    experience: int = Query(...),
    db: Session = Depends(get_db)
):
    questions = db.query(Question).filter(
        Question.role == role,
        Question.min_experience <= experience,
        Question.max_experience >= experience
    ).all()

    return [
        {
            "id": q.id,
            "question": q.question,
            "expected_answer": q.expected_answer
        }
        for q in questions
    ]