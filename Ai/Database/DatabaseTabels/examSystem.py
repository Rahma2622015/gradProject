from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base


class ExamSystem(Base):
    __tablename__ = "exam_systems"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    exam_type = Column(String, nullable=False)
    content = Column(String, nullable=False)
    exam_type_arabic = Column(String, nullable=False)
    content_arabic = Column(String, nullable=False)

    course = relationship("Course", back_populates="exam_systems")
