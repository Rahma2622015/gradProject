from Database.session import SessionLocal
from Database.DatabaseTabels.course import Course

class CourseHours:
    def __init__(self):
        self.session = SessionLocal()


    def get_course_hours(self, course_name):
        course = self.session.query(Course).filter(
            Course.name.ilike(f"%{course_name}%") |
            Course.short_name.ilike(f"%{course_name}%") |
            Course.code.ilike(f"%{course_name}%") |
            Course.name_arabic.ilike(f"%{course_name}%")|
            Course.short_name_arabic.ilike(f"%{course_name}%")
        ).first()

        if course:
            return course.course_hours
        else:
            return None