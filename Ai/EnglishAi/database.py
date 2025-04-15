from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "sqlite:///university_information.db"
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

course_professor = Table(
    'course_professor',
    Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id')),
    Column('professor_id', Integer, ForeignKey('professors.id'))
)


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    short_name = Column(String)
    code = Column(String, unique=True, nullable=False)

    professors = relationship("Professor", secondary=course_professor, back_populates="courses")
    questions = relationship("CourseQuestion", back_populates="course")


class CourseQuestion(Base):
    __tablename__ = "course_questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    course_id = Column(Integer, ForeignKey('courses.id'))

    course = relationship("Course", back_populates="questions")
    answers = relationship("Answers", back_populates="question")


class Answers(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    answer = Column(String)
    score = Column(Integer, nullable=False)
    question_id = Column(Integer, ForeignKey('course_questions.id'))

    question = relationship("CourseQuestion", back_populates="answers")



class Professor(Base):
    __tablename__ = 'professors'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)

    courses = relationship("Course", secondary=course_professor, back_populates="professors")


Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

