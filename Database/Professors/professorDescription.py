from Database.database import SessionLocal, Professor

class ProfessorDescription:
    def __init__(self):
        self.session = SessionLocal()

    def get_professor_info(self, professor_name) :
        professor = self.session.query(Professor).filter(
            Professor.name.ilike(f"%{professor_name}%")|
            Professor.name_arabic.ilike(f"%{professor_name}%")
        ).first()

        if not professor:
            return "Professor not found. Please check the spelling or try another name."
        elif professor and professor.name_arabic and professor_name in professor.name_arabic:

            return professor.description_arabic
        else:
            return professor.description