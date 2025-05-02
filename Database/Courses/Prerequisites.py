from Database.database import SessionLocal, Course

class CoursePrerequisites:
    def __init__(self):
        self.session = SessionLocal()


    def get_course_prerequisite(self, course_name):
        course = self.session.query(Course).filter(
            Course.name.ilike(f"%{course_name}%") |
            Course.short_name.ilike(f"%{course_name}%") |
            Course.code.ilike(f"%{course_name}%") |
            Course.name_arabic.ilike(f"%{course_name}%")
        ).first()

        if course.code and course_name in course.code:
            return [p.code for p in course.prerequisites]
        elif course.name_arabic and course_name in course.name_arabic:
            return [p.name_arabic for p in course.prerequisites]
        elif course.name and course_name in course.name:
            return [p.name for p in course.prerequisites]
        elif course.short_name and course_name in course.short_name:
            return [p.short_name for p in course.prerequisites]
        else:
            return [p.code for p in course.prerequisites]