from Database.session import SessionLocal
from Database.DatabaseTabels.course import Course
from Database.DatabaseTabels.department import Department

class CourseDepartment:
    def __init__(self):
        self.session = SessionLocal()

    def get_department_of_course(self, course_name, language: str = "en"):
        course = self.session.query(Course).filter(
            Course.name.ilike(f"%{course_name}%") |
            Course.short_name.ilike(f"%{course_name}%") |
            Course.code.ilike(f"%{course_name}%") |
            Course.name_arabic.ilike(f"%{course_name}%")|
            Course.short_name_arabic.ilike(f"%{course_name}%")
        ).first()
        department= self.session.query(Department).filter(Department.id ==course.department_id).first()

        if not department or not course:
            return None

        if course and department:
            if language == "ar":
                return department.name_arabic
            else:
                return department.name


