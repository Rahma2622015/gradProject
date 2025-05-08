from Database.Datastorage_DB import DatabaseStorage
from Modules.dataStorage import DataStorage
from Database.FetchDataCourses.coureExamSystem import CourseAssistant
from Database.FetchDataProfessors.professorExamSystem import CourseAssistantPr
from Ai.ArabicAi.ArabicPreprocessor import ArabicPreprocessor

class ArSingleShotRecommendationSystem:
    def __init__(self, data_storage: DatabaseStorage, memory: DataStorage
                 , DS: CourseAssistant,Dsbe:CourseAssistantPr):
        self.data_storage = data_storage
        self.memory = memory
        self.DSb = DS
        self.Dsbe=Dsbe
        self.pre = ArabicPreprocessor()

    def handle_user_message(self, message):
        course_name = self.pre.extract_course_name_from_tags(message)
        professor_name = self.pre.extract_person_name_from_tags(message)
        print(f"[INFO] Detected course name: {course_name}, Detected professor name: {professor_name}")

        if course_name:
            exam_data = self.get_exam_system_for_course(course_name)
            if not exam_data:
                return f"عذرًا، لم أتمكن من العثور على نظام الامتحان للمقرر {course_name}", []
            return f"هذا هو نظام الامتحان الخاص بالمقرر {course_name}\n{exam_data}", []

        elif professor_name:
            exam_data = self.get_exam_system_for_professor(professor_name)
            if not exam_data:
                return f"عذرًا، لم أتمكن من العثور على نظام الامتحان للدكتور {professor_name}", []
            return f"هذا هو نظام الامتحان الخاص بالدكتور {professor_name}\n{exam_data}", []

        else:
            return "عذرًا، لم أتمكن من التعرف على اسم المقرر أو اسم الدكتور من رسالتك", []

    def get_exam_system_for_course(self, course_name: str):
        exam_system = self.DSb.get_exam_system_by_course_name(course_name,"ar")

        if not exam_system :
            return "لا يوجد نظام امتحانات لهذا الكورس."
        return exam_system

    def get_exam_system_for_professor(self, professor_name: str):
        exam_system = self.Dsbe.get_exam_system_by_professor_name(professor_name,"ar")
        if not exam_system:
            return "لا يوجد نظام امتحانات لهذا الدكتور."
        return exam_system
