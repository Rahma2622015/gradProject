from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

course_ta = Table(
    'course_ta',
    Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id')),
    Column('ta_id', Integer, ForeignKey('teaching_assistants.id'))
)

class TeachingAssistant(Base):
    __tablename__ = 'teaching_assistants'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)

    name_arabic = Column(String, nullable=True)
    description_arabic = Column(String, nullable=True)

    courses = relationship("Course", secondary=course_ta, back_populates="assistants")
