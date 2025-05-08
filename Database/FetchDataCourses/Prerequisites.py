from Database.FetchDataCourses.findCourse import FindCourse

class CoursePrerequisites:
    def __init__(self):
        self.find=FindCourse()

    def get_course_prerequisite(self, course_name,language: str = "en"):
        course =self.find._find_course(course_name)

        if course:
            if language == "ar":
                if course.name_arabic and course_name in course.name_arabic:
                    return [p.name_arabic for p in course.prerequisites]
                elif course.short_name_arabic and course_name in course.short_name_arabic:
                    return [p.short_name_arabic for p in course.prerequisites]
            else:
                if course.code and course_name in course.code:
                    return [p.code for p in course.prerequisites]
                elif course.name and course_name in course.name:
                    return [p.name for p in course.prerequisites]
                elif course.short_name and course_name in course.short_name:
                    return [p.short_name for p in course.prerequisites]
        else:
            return None