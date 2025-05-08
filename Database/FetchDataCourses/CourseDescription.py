from Database.session import SessionLocal
from Database.FetchDataCourses.findCourse import FindCourse

class CourseDescription:
    def __init__(self):
        self.finder = FindCourse()

    def get_course_description(self, course_name, language: str = "en"):
        course = self.finder._find_course(course_name)

        if not course:
            return "لم يتم العثور على المادة" if language == "ar" else "Course not found"

        name = course.name_arabic if language == "ar" else course.name
        description = course.description_arabic if language == "ar" else course.description
        prefix = "مادة" if language == "ar" else "Course"

        return f"{prefix} {name}: {description if description else ('لا يوجد وصف' if language == 'ar' else 'No description')}"
