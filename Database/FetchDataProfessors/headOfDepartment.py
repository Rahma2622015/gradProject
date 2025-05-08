from Database.session import SessionLocal
from Database.DatabaseTabels.department import Department
from Levenshtein import distance


class HeadDepartment:
    def __init__(self):
        self.session = SessionLocal()

    def get_head_of_department(self, department_name, language: str = "en"):
        departments = self.session.query(Department).all()
        closest_match = None
        min_dist = float('inf')

        for dept in departments:
            for name_variant in [dept.name, dept.name_arabic]:
                if name_variant:
                    dist = distance(department_name.lower(), name_variant.lower())
                    if dist < min_dist and dist <= 2:
                        closest_match = dept
                        min_dist = dist

        if closest_match:
            return closest_match.head_name_arabic if language == "ar" else closest_match.head_name

        return None


