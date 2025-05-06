from Database.session import SessionLocal
from Database.DatabaseTabels.course import Course

class CourseAssistant:
    def __init__(self):
        self.session = SessionLocal()

    def get_exam_system_by_course_name(self, course_name: str, language: str = "en"):
        course = self.session.query(Course).filter(
            Course.name.ilike(course_name)|
            Course.short_name.ilike(course_name) |
            Course.code.ilike(course_name) |
            Course.name_arabic.ilike(course_name) |
            Course.short_name_arabic.ilike(course_name)
        ).first()
        if not course:
            return None

        if course.exam_system:
            if language=="ar":
                return course.exam_system.course_system_arabic
            else:
                return course.exam_system.course_system
        else:
            return None
