from Database.session import SessionLocal
from Database.DatabaseTabels.course import Course
from Database.DatabaseTabels.examSystem import CourseExamSystem

class CourseSystem:
    def __init__(self):
        self.session = SessionLocal()

    def get_exam_system_by_course_name(self, course_name: str, language: str = "en"):
        course = self.session.query(Course).filter(
            Course.name.ilike(f"%{course_name}%") |
            Course.short_name.ilike(f"%{course_name}%") |
            Course.code.ilike(f"%{course_name}%") |

            Course.name_arabic.ilike(f"%{course_name}%") |

            Course.short_name_arabic.ilike(f"%{course_name}%")
        ).first()

        if not course:
            return None

        exam_system = self.session.query(CourseExamSystem).filter(CourseExamSystem.course_id == course.id).first()
        if not exam_system:
            return None

        if language == "ar":
            return exam_system.course_system_arabic
        return exam_system.course_system

