from Database.FetchDataCourses.findCourse import FindCourse

class CourseHours:
    def __init__(self):
        self.find = FindCourse()

    def get_course_hours(self, course_name):
        course =self.find._find_course(course_name)
        if course:
            return course.course_hours
        else:
            return None


