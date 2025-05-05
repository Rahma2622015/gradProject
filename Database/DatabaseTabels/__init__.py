from .database import Base
from .course import Course
from .professor import Professor, course_professor
from .assistant import TeachingAssistant, course_ta
from .department import Department
from .question import CourseQuestion, Answers
