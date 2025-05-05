from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class CourseQuestion(Base):
    __tablename__ = "course_questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    question_arabic = Column(String, nullable=True)
    course_id = Column(Integer, ForeignKey('courses.id'))

    course = relationship("Course", back_populates="questions")
    answers = relationship("Answers", back_populates="question")


class Answers(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    answer = Column(String)
    answer_arabic = Column(String, nullable=True)
    score = Column(Integer, nullable=False)
    question_id = Column(Integer, ForeignKey('course_questions.id'))

    question = relationship("CourseQuestion", back_populates="answers")
