from Database.session import SessionLocal
from Database.DatabaseTabels.department import Department

class HeadDepartment:
    def __init__(self):
        self.session = SessionLocal()

    def get_head_of_department(self, department_name, language: str = "en"):
        department = self.session.query(Department).filter(
            (Department.name.ilike(f"%{department_name}%")) |
            (Department.name_arabic.ilike(f"%{department_name}%"))
        ).first()

        if department:
            if language=="ar":
                return department.head_name_arabic
            else:
                return department.head_name

        return None

