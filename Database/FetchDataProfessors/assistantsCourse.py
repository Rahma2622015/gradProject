from Database.FetchDataCourses.findCourse import FindCourse

class AssistantCourse:
    def __init__(self):
        self.finder = FindCourse()

    def get_assistants_of_course(self, course_name, language: str = "en"):
        course = self.finder._find_course(course_name)

        if not course:
            return "لم يتم العثور على المادة" if language == "ar" else "Course not found"

        name = course.name_arabic if language == "ar" else course.name
        assistants = [a.name_arabic if language == "ar" else a.name for a in course.assistants]

        prefix = "معيد المادة" if language == "ar" else "Assistants of course"
        no_assistants_msg = "لا يوجد معيدون" if language == "ar" else "No assistants"

        return f"{prefix} {name}: {', '.join(assistants) if assistants else no_assistants_msg}"
