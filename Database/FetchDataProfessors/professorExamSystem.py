from Database.session import SessionLocal
from Database.DatabaseTabels.professor import Professor
from Database.DatabaseTabels.examSystem import ProfessorExamSystem

class ProfessorSystem:

    def __init__(self):
        self.session = SessionLocal()

    def get_exam_system_by_professor_name(self, professor_name: str, language: str = "en"):
        professor = self.session.query(Professor).filter(

            Professor.name.ilike(f"%{professor_name}%") |
            Professor.name_arabic.ilike(f"%{professor_name}%")
        ).first()
        if not professor:
            return None

        exam_system = self.session.query(ProfessorExamSystem).filter(ProfessorExamSystem.professor_id == professor.id).first()

        if not exam_system:
            return None
        if language=="ar":
            return exam_system.professor_system_arabic
        return  exam_system.professor_system
