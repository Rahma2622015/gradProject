from Database.FetchDataCourses.findCourse import FindCourse



class CourseDepartment:
    def __init__(self):
        self.find = FindCourse()

    def get_department_of_course(self, course_name, language: str = "en"):
        course =self.find._find_course(course_name)
        if course and course.department:
            if language == "ar":
                return department.name_arabic
            else:
                return department.name











