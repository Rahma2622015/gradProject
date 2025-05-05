from Database.session import SessionLocal
from Database.DatabaseTabels.course import Course

class CourseDepartment:
    def __init__(self):
        self.session = SessionLocal()

    def get_department_of_course(self, course_name, language: str = "en"):
        course = self.session.query(Course).filter(
            Course.name == course_name|
            Course.name_arabic == course_name |
            Course.short_name == course_name |
            Course.short_name_arabic == course_name |
            Course.code == course_name
        ).first()
        if course and course.department:
            if language == "ar":
                return course.department.name_arabic
            else:
                return course.department.name
        return None

