from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)

    responses = relationship("Response", back_populates="session")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    question = Column(String)
    expected_answer = Column(String)

    role = Column(String)               # e.g. "software_engineer"
    min_experience = Column(Integer)
    max_experience = Column(Integer)


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(Integer, ForeignKey("sessions.id"))
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=True)

    # keep text for flexibility (important)
    question = Column(String)
    transcript = Column(String)

    audio_metrics = Column(JSON)
    video_metrics = Column(JSON)
    evaluation = Column(JSON)

    session = relationship("Session", back_populates="responses")