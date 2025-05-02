from Database.Courses.courseHours import CourseHours
from Database.Courses.courseDegree import CourseDegree
from Database.Courses.CourseDescription import CourseDescription
from Database.Courses.Prerequisites import CoursePrerequisites
from Database.Courses.QuestionsAndAnswers import CourseQuestionsAndAnswers
from Database.Professors.professorDescription import ProfessorDescription

class DatabaseStorage:
    def __init__(self):
        self.courseHour=CourseHours()
        self.courseDegree=CourseDegree()
        self.courseDes=CourseDescription()
        self.coursePre=CoursePrerequisites()
        self.courseQuestion = CourseQuestionsAndAnswers()
        self.professors = ProfessorDescription()

