from Database.database import SessionLocal, Course

class CourseDescription:
    def __init__(self):
        self.session = SessionLocal()

    def get_course_description(self, course_name) -> str:
        course = self.session.query(Course).filter(
            Course.name_arabic.ilike(f"%{course_name}%")|
            Course.name.ilike(f"%{course_name}%")|
            Course.short_name.ilike(f"%{course_name}%") |
            Course.short_name_arabic.ilike(f"%{course_name}%") |
            Course.code.ilike(f"%{course_name}%")
        ).first()

        if course and (course.name_arabic and course_name in course.name_arabic or
                       course.short_name_arabic and course_name in course.short_name_arabic):

            return course.description_arabic if course else "المادة ليست موجودة في الداتابيز!"
        else:
            return course.description if course else "Course not found."