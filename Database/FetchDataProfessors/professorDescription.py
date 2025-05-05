from Database.session import SessionLocal
from Database.DatabaseTabels.professor import Professor

class ProfessorDescription:
    def __init__(self):
        self.session = SessionLocal()

    def get_professor_info(self, professor_name, language: str = "en") :
        professor = self.session.query(Professor).filter(
            Professor.name.ilike(f"%{professor_name}%")|
            Professor.name_arabic.ilike(f"%{professor_name}%")
        ).first()

        if  professor:
            if language=="ar":
                return professor.description_arabic
            return professor.description

        return []