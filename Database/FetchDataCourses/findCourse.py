from Database.session import SessionLocal
from Database.DatabaseTabels.course import Course
from Database.utils import get_closest_match

class FindCourse:
    def __init__(self):
        self.session = SessionLocal()

    def _find_course(self, name):
        course_by_code = self.session.query(Course).filter(
            Course.code.ilike(f"%{name}%")
        ).first()
        if course_by_code:
            return course_by_code

        courses = self.session.query(Course).filter(
            Course.name_arabic.ilike(f"%{name}%") |
            Course.name.ilike(f"%{name}%") |
            Course.short_name.ilike(f"%{name}%") |
            Course.short_name_arabic.ilike(f"%{name}%")
        ).all()

        if len(courses) == 1:
            return courses[0]
        elif len(courses) > 1:
            return courses[0]

        all_courses = self.session.query(Course).all()
        names = [c.name for c in all_courses if c.name] + \
                [c.short_name for c in all_courses if c.short_name] + \
                [c.name_arabic for c in all_courses if c.name_arabic] + \
                [c.short_name_arabic for c in all_courses if c.short_name_arabic]

        matched = get_closest_match(name, names)
        if not matched:
            return None

        return self.session.query(Course).filter(
            Course.name.ilike(f"%{matched}%") |
            Course.short_name.ilike(f"%{matched}%") |
            Course.code.ilike(f"%{matched}%") |
            Course.name_arabic.ilike(f"%{matched}%") |
            Course.short_name_arabic.ilike(f"%{matched}%")
        ).first()
