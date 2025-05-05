from Database.Datastorage_DB import DatabaseStorage
from Modules.dataStorage import DataStorage
from Database.FetchDataCourses.QuestionsAndAnswers import CourseQuestionsAndAnswers
from Ai.EnglishAi.Tokeniztion import Tokenizers

class SingleShotRecommendationSystem:
    def __init__(self, data_storage: DatabaseStorage, memory: DataStorage, DS: CourseQuestionsAndAnswers):
        self.data_storage = data_storage
        self.memory = memory
        self.DSb = DS
        self.tokenizer = Tokenizers()

    def handle_user_message(self, message: str):
        # Step 1: Extract course name or professor name from user message
        course_name = self.tokenizer.extract_course_name(message)
        professor_name = self.tokenizer.extract_professor_name(message)
        print(f"[INFO] Detected course name: {course_name}, Detected professor name: {professor_name}")

        # Step 2: Check if it's asking about a course or a professor
        if course_name:
            exam_data = self.get_exam_system_for_course(course_name)
            if not exam_data:
                return f"Sorry, I couldn't find an exam system for the course '{course_name}'.", []
            return f"Here is the exam system for the course '{course_name}': {exam_data}", []

        elif professor_name:
            exam_data = self.get_exam_system_for_professor(professor_name)
            if not exam_data:
                return f"Sorry, I couldn't find an exam system for Dr. {professor_name}.", []
            return f"Here is the exam system for Dr. {professor_name}: {exam_data}", []

        else:
            return "Sorry, I couldn't identify the course or professor name from your message.", []

    def get_exam_system_for_course(self, course_name: str):
        # Query the database to find the exam system for the provided course name
        exam_system = self.DSb.get_course_exam_system(course_name)

        if not exam_system or isinstance(exam_system, str):
            return "No exam system found for this course."
        return exam_system

    def get_exam_system_for_professor(self, professor_name: str):
        # Query the database to find the exam system for the provided professor name
        exam_system = self.DSb.get_professor_exam_system(professor_name)

        if not exam_system or isinstance(exam_system, str):
            return "No exam system found for this professor."
        return exam_system
