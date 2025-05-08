from Database.session import SessionLocal
from Database.DatabaseTabels.professor import Professor
from Database.utils import get_closest_match

class FindProfessor:
    def __init__(self):
        self.session = SessionLocal()

    def _find_professor(self, professor_name):
        professors = self.session.query(Professor).filter(
            Professor.name.ilike(f"%{professor_name}%") |
            Professor.name_arabic.ilike(f"%{professor_name}%")
        ).all()

        if not professors:
            all_professors = self.session.query(Professor).all()
            names = ([p.name for p in all_professors if p.name] +
                     [p.name_arabic for p in all_professors if p.name_arabic])
            matched_name = get_closest_match(professor_name, names)
            if matched_name:
                professors = self.session.query(Professor).filter(
                    Professor.name.ilike(f"%{matched_name}%") |
                    Professor.name_arabic.ilike(f"%{matched_name}%")
                ).all()

        return professors
