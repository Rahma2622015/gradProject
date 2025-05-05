from Database.session import SessionLocal
from Database.DatabaseTabels.assistant import TeachingAssistant
from Database.DatabaseTabels.course import Course

class CourseAssistant:
    def __init__(self):
        self.session = SessionLocal()

    def get_courses_of_assistant(self, assistant_name, language: str = "en"):
        assistant = (self.session.query(TeachingAssistant).filter(
            (TeachingAssistant.name.ilike(f"%{assistant_name}%")) |
            (TeachingAssistant.name_arabic.ilike(f"%{assistant_name}%"))
        ).first())

        if assistant:
            if language == "ar":
                return [course.name_arabic for course in assistant.courses]
            else:
                return [course.code for course in assistant.courses]
        return []

    def get_assistants_of_course(self, course_code, language: str = "en"):
        course = self.session.query(Course).filter(Course.code == course_code).first()
        if course:
            if language == "ar":
                return [assistant.name_arabic for assistant in course.assistants]
            else:
                return [assistant.name for assistant in course.assistants]
        return []

