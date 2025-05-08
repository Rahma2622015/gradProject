from Database.FetchDataCourses.findCourse import FindCourse

class CourseDegree:
    def __init__(self):
        self.find = FindCourse()

    def get_course_degree(self, course_name):
        course =self.find._find_course(course_name)
        if course:
            return course.course_degree
        else:
            return None






