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
    short_name_arabic = Column(String, nullable=True)
    code = Column(String, unique=True, nullable=False)
    course_hours=Column(Integer, nullable=True)
    course_degree=Column(Integer, nullable=True)
    name_arabic = Column(String, nullable=True)
    description_arabic = Column(String, nullable=True)

    professors = relationship("Professor", secondary=course_professor, back_populates="courses")
    questions = relationship("CourseQuestion", back_populates="course")
    exam_systems = relationship('ExamSystem', back_populates='course')

    prerequisites = relationship(
        'Course',
        secondary=course_prerequisites,
        primaryjoin=id == course_prerequisites.c.course_id,
        secondaryjoin=id == course_prerequisites.c.prerequisite_id,
        backref='required_for'
    )


class CourseQuestion(Base):
    __tablename__ = "course_questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    course_id = Column(Integer, ForeignKey('courses.id'))

    question_arabic = Column(String, nullable=True)

    course = relationship("Course", back_populates="questions")
    answers = relationship("Answers", back_populates="question")


class Answers(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    answer = Column(String)
    score = Column(Integer, nullable=False)
    question_id = Column(Integer, ForeignKey('course_questions.id'))

    answer_arabic = Column(String, nullable=True)

    question = relationship("CourseQuestion", back_populates="answers")


class Professor(Base):
    __tablename__ = 'professors'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)

    name_arabic = Column(String, nullable=True)
    description_arabic = Column(String, nullable=True)

    courses = relationship("Course", secondary=course_professor, back_populates="professors")

class ExamSystem(Base):
    __tablename__ = "exam_systems"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    exam_type = Column(String, nullable=False)
    content = Column(String, nullable=False)
    exam_type_arabic = Column(String, nullable=False)
    content_arabic = Column(String, nullable=False)

    course = relationship("Course", back_populates="exam_systems")


Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
