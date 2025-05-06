from Database.session import SessionLocal
from Database.DatabaseTabels.professor import Professor

class CourseAssistant:
    def __init__(self):
        self.session = SessionLocal()

    def get_exam_system_by_professor_name(self, professor_name: str, language: str = "en"):
        professor = self.session.query(Professor).filter(
            Professor.name.ilike(professor_name)|
            Professor.name_arabic.ilike(professor_name)
        ).first()
        if not professor:
            return None

        if professor.exam_system:
            if language=="ar":
                return professor.exam_system.professor_system_arabic
            else:
                return professor.exam_system.professor_system
        else:
            return None
