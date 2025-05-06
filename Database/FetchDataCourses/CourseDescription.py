from Database.session import SessionLocal
from Database.DatabaseTabels.course import Course

class CourseDescription:
    def __init__(self):
        self.session = SessionLocal()

    def get_course_description(self, course_name,language: str = "en") :
        course = self.session.query(Course).filter(
            Course.name_arabic.ilike(f"%{course_name}%")|
            Course.name.ilike(f"%{course_name}%")|
            Course.short_name.ilike(f"%{course_name}%") |
            Course.short_name_arabic.ilike(f"%{course_name}%") |
            Course.code.ilike(f"%{course_name}%")
        ).first()

        if course :
            if language=="ar":
                return course.description_arabic if course else "المادة ليست موجودة في الداتابيز!"

            return course.description
        return None