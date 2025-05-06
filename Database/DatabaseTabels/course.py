from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base
from .professor import course_professor
from .assistant import course_ta

course_prerequisites = Table(
    'course_prerequisites',
    Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id')),
    Column('prerequisite_id', Integer, ForeignKey('courses.id'))
)

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    short_name = Column(String)
    code = Column(String, unique=True, nullable=False)
    course_hours = Column(Integer, nullable=True)
    course_degree = Column(Integer, nullable=True)
    name_arabic = Column(String, nullable=True)
    short_name_arabic = Column(String, nullable=True)
    description_arabic = Column(String, nullable=True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=True)


    professors = relationship("Professor", secondary=course_professor, back_populates="courses")
    assistants = relationship("TeachingAssistant", secondary=course_ta, back_populates="courses")
    questions = relationship("CourseQuestion", back_populates="course")
    department = relationship("Department", back_populates="courses")
    exam_system = relationship("CourseExamSystem", back_populates="course", uselist=False)
    prerequisites = relationship(
        'Course',
        secondary=course_prerequisites,
        primaryjoin=id == course_prerequisites.c.course_id,
        secondaryjoin=id == course_prerequisites.c.prerequisite_id,
        backref='required_for'
    )
