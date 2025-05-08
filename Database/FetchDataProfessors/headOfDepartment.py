from Database.session import SessionLocal
from Database.DatabaseTabels.department import Department
from Database.utils import get_closest_match

class HeadDepartment:
    def __init__(self):
        self.session = SessionLocal()

    def get_head_of_department(self, department_name, language: str = "en"):
        department = self.session.query(Department).filter(
            (Department.name.ilike(f"%{department_name}%")) |
            (Department.name_arabic.ilike(f"%{department_name}%"))
        ).first()

        if department:
            return department.head_name_arabic if language == "ar" else department.head_name

        departments = self.session.query(Department).all()
        names = [a.name for a in departments if a.name] + [a.name_arabic for a in departments if a.name_arabic]

        matched_name = get_closest_match(department_name, names)
        if not matched_name:
            return None

        department = self.session.query(Department).filter(
            Department.name == matched_name or
            Department.name_arabic == matched_name
        ).first()

        if department:
            return department.head_name_arabic if language == "ar" else department.head_name

        return None


