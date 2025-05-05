from Database.FetchDataCourses.courseAssistant import CourseAssistant
from Database.FetchDataCourses.courseDepartment import CourseDepartment
from Database.FetchDataCourses.courseProfessor import CourseProfessor
from Database.FetchDataCourses.courseHours import CourseHours
from Database.FetchDataCourses.courseDegree import CourseDegree
from Database.FetchDataCourses.CourseDescription import CourseDescription
from Database.FetchDataCourses.Prerequisites import CoursePrerequisites
from Database.FetchDataCourses.QuestionsAndAnswers import CourseQuestionsAndAnswers
from Database.FetchDataProfessors.Assistants import Assistant
from Database.FetchDataProfessors.headOfDepartment import HeadDepartment
from Database.FetchDataProfessors.professorDescription import ProfessorDescription

class DatabaseStorage:
    def __init__(self):
        self.courseHour=CourseHours()
        self.courseDegree=CourseDegree()
        self.courseDes=CourseDescription()
        self.coursePre=CoursePrerequisites()
        self.courseAssistant=CourseAssistant()
        self.courseDepartment=CourseDepartment()
        self.courseProfessor=CourseProfessor()
        self.courseQuestion = CourseQuestionsAndAnswers()
        self.professors = ProfessorDescription()
        self.assistant = Assistant()
        self.head_department = HeadDepartment()

