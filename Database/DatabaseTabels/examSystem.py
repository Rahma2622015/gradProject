from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class CourseExamSystem(Base):
    __tablename__ = "course_exam_systems"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    course_system = Column(String, nullable=False)
    course_system_arabic = Column(String, nullable=False)


    course = relationship("Course", back_populates="exam_system")



class ProfessorExamSystem(Base):
    __tablename__ = "professor_exam_systems"

    id = Column(Integer, primary_key=True)
    professor_id = Column(Integer, ForeignKey("professors.id"), nullable=False)

    professor_system= Column(String, nullable=False)
    professor_system_arabic = Column(String, nullable=False)

    professor = relationship("Professor", back_populates="exam_system")
