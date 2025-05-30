from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base
from Database.DatabaseTabels.examSystem import ProfessorExamSystem

course_professor = Table(
    'course_professor',
    Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id')),
    Column('professor_id', Integer, ForeignKey('professors.id'))
)

class Professor(Base):
    __tablename__ = 'professors'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)

    name_arabic = Column(String, nullable=True)
    description_arabic = Column(String, nullable=True)

    courses = relationship("Course", secondary=course_professor, back_populates="professors")

Professor.exam_system = relationship("ProfessorExamSystem", back_populates="professor", uselist=False)
ProfessorExamSystem.professor = relationship("Professor", back_populates="exam_system")