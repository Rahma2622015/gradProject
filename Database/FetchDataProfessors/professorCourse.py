from Database.FetchDataCourses.findCourse import FindCourse

class ProfessorCourse:
    def __init__(self):
        self.finder = FindCourse()

    def get_professors_of_course(self, course_name, language="en"):
        course = self.finder._find_course(course_name)

        if not course:
            return "لم يتم العثور على المادة" if language == "ar" else "Course not found"

        name = course.name_arabic if language == "ar" else course.name
        professors = [p.name_arabic if language == "ar" else p.name for p in course.professors]

        prefix = "دكاترة المادة" if language == "ar" else "Professors of course"
        no_professors_msg = "لا يوجد دكاترة" if language == "ar" else "No professors"

        return f"{prefix} {name}: {', '.join(professors) if professors else no_professors_msg}"
