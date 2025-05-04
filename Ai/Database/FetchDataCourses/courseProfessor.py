from Database.session import SessionLocal
from Database.DatabaseTabels.course import Course
from Database.DatabaseTabels.professor import Professor

class CourseProfessor:
    def __init__(self):
        self.session = SessionLocal()

    def get_professors_of_course(self, course_name, language="en"):
        course = self.session.query(Course).filter(
            Course.name.ilike(f"%{course_name}%") |
            Course.short_name.ilike(f"%{course_name}%") |
            Course.code.ilike(f"%{course_name}%") |
            Course.name_arabic.ilike(f"%{course_name}%")
        ).first()
        if course:
            if language == "ar":
                return [prof.name_arabic for prof in course.professors if prof.name_arabic]
            else:
                return [prof.name for prof in course.professors]
        return []

    def get_courses_of_professor(self, prof_name, language="en"):
        professor = self.session.query(Professor).filter(
            Professor.name.ilike(f"%{prof_name}%") |
            Professor.name_arabic.ilike(f"%{prof_name}%")
        ).first()
        if professor:
            if language == "ar":
                return [course.name_arabic for course in professor.courses if course.name_arabic]
            else:
                return [course.code for course in professor.courses]
        return []
