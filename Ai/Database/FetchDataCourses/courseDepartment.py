from Database.session import SessionLocal
from Database.DatabaseTabels.course import Course

class CourseDepartment:
    def __init__(self):
        self.session = SessionLocal()

    def get_department_of_course(self, course_code, language: str = "en"):
        course = self.session.query(Course).filter(Course.code == course_code).first()
        if course and course.department:
            if language == "ar":
                return course.department.name_arabic
            else:
                return course.department.name
        return None

