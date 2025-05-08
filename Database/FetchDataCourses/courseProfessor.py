from Database.FetchDataProfessors.findProfessor import FindProfessor

class CourseProfessor:
    def __init__(self):
        self.finder = FindProfessor()

    def get_courses_of_professor(self, prof_name, language: str = "en"):
        professors = self.finder._find_professor(prof_name)

        if not professors:
            return None

        results = []
        for prof in professors:
            if language == "ar":
                courses = [course.name_arabic for course in prof.courses if course.name_arabic]
                results.append(f"الدكتور {prof.name_arabic} : يُدرِّس {', '.join(courses) if courses else 'لا توجد مواد'}")
            else:
                courses = [course.code for course in prof.courses if course.code]
                results.append(f"Professor {prof.name}  teach : {', '.join(courses) if courses else 'No courses found'}")

        if len(results) == 1:
            return results[0]
        else:
            return "\n".join(results)
