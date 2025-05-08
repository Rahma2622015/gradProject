from Database.Datastorage_DB import DatabaseStorage
from Modules.dataStorage import DataStorage
from Database.FetchDataCourses.coureExamSystem import CourseSystem
from Database.FetchDataProfessors.professorExamSystem import ProfessorSystem
from Ai.EnglishAi.Tokeniztion import Tokenizers

class SingleShotRecommendationSystem:
    def __init__(self, data_storage: DatabaseStorage, memory: DataStorage
                 , DS: CourseSystem , Dsbe:ProfessorSystem):
        self.data_storage = data_storage
        self.memory = memory
        self.DSb = DS
        self.Dsbe=Dsbe
        self.tokenizer = Tokenizers()

    def handle_user_message(self, message: str):
        course_name = self.tokenizer.extract_course_name(message)
        professor_name = self.tokenizer.extract_person_name_from_tags(message)
        print(f"[INFO] Detected course name: {course_name}, Detected professor name: {professor_name}")

        if course_name:
            exam_data = self.get_exam_system_for_course(course_name)
            if not exam_data:
                return f"Sorry, I couldn't find an exam system for the course {course_name}.", []
            return f"Here is the exam system for the course {course_name}: {exam_data}", []

        elif professor_name:
            exam_data = self.get_exam_system_for_professor(professor_name)
            if not exam_data:
                return f"Sorry, I couldn't find an exam system for Dr. {professor_name}.", []
            return f"Here is the exam system for Dr. {professor_name}: {exam_data}", []

        else:
            return "Sorry, I couldn't identify the course or professor name from your message.", []

    def get_exam_system_for_course(self, course_name: str):
        exam_system = self.DSb.get_exam_system_by_course_name(course_name,"en")

        if not exam_system :
            return "No exam system found for this course."
        return exam_system

    def get_exam_system_for_professor(self, professor_name: str):
        exam_system = self.Dsbe.get_exam_system_by_professor_name(professor_name,"en")
        if not exam_system :
            return "No exam system found for this professor."
        return exam_system
