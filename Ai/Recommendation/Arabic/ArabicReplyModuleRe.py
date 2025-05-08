import json
from random import choice
from Ai.Recommendation.Arabic.ArabicRecomExamSystem import ArRecommendation
from Ai.EnglishAi.chattask import ChatTask
from Ai.Recommendation.Arabic.ArabicCoursesystem import ArRecommendationSystem
from Ai.EnglishAi.Tokeniztion import Tokenizers
from Database.Datastorage_DB import DatabaseStorage
from Modules import DataStorage
from Ai.Recommendation.Arabic.arabicRecomMulticourses import ArMultiCourseRecommendationSystem
from Database.FetchDataCourses.QuestionsAndAnswers import CourseQuestionsAndAnswers
from Ai.ArabicAi.ArabicPreprocessor import ArabicPreprocessor
from Ai.Recommendation.Arabic.ArabExamCourseSys import ArSingleShotRecommendationSystem
from Database.FetchDataCourses.coureExamSystem import CourseSystem
from Database.FetchDataProfessors.professorExamSystem import ProfessorSystem
import variables

data_storage = DatabaseStorage()
memory = DataStorage()
dbs=CourseQuestionsAndAnswers()
dbcour=CourseSystem()
dbpro=ProfessorSystem()

class ArReplyModuleRe:
    def __init__(self, json_path=variables.ArResponseDataLocationRE, memory_db=None, temp_storage=None):
        self.load_responses(json_path)
        self.recommender = ArRecommendation()
        self.course_dynamic_recommender = ArRecommendationSystem(memory_db, temp_storage,dbs)
        self.tokenizer = Tokenizers()
        self.pre = ArabicPreprocessor()
        self.course_selection_recommender = ArMultiCourseRecommendationSystem(
             data_storage, memory, ArRecommendationSystem(memory_db, temp_storage,dbs)
         )
        self.CourseExam=ArSingleShotRecommendationSystem(data_storage, memory,dbcour,dbpro)
    def load_responses(self, json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                self.data = json.load(file)
            print(f"[INFO] arabic Response file loaded successfully: {json_path}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERROR] Failed to load arabic response file: {e}")
            self.data = {}

    def generate_responseR(self, reply, user_input):
        s = ""
        options = []

        for r in reply:
            if isinstance(r, tuple) and len(r) > 0:
                if r[0] == ChatTask.ExamSystem:
                    response = self.recommender.handle_exam_recommendation(user_input)

                    if isinstance(response, tuple) and len(response) == 2:
                        s, options = response
                    elif isinstance(response, str):
                        s = response
                        options = []
                    else:
                        print(f"[ERROR] Unexpected response format: {response}")
                        s = "حدث خطأ أثناء معالجة التوصية الخاصة بك."
                        options = []

                elif r[0] == ChatTask.CourseSystem:
                    course_name = self.pre.extract_course_name(user_input)
                    print(f"[INFO] تم التعرف على اسم المادة: {course_name}")
                    if course_name:
                        response, options = self.course_dynamic_recommender.start_recommendation(course_name)
                        if isinstance(response, str):
                            s = response
                            options = []
                        else:
                            print(f"[ERROR] Unexpected course recommendation format: {response}")
                            s = "حدث خطأ أثناء معالجة التوصية بالمادة."
                            options = []
                    else:
                        s = "عذرًا، لم أتمكن من استخراج اسم المادة من سؤالك."

                elif r[0] == ChatTask.MultiCourseRecommendationTask:
                    course_names = self.tokenizer.extract_all_course_names(user_input)
                    print(f"[INFO] تم التعرف على أسماء المواد: {course_names}")
                    if course_names:
                        response, options = self.course_selection_recommender.start(course_names)
                        if isinstance(response, str):
                            s = response
                            options = []
                        else:
                            s = "حدث خطأ أثناء معالجة توصية المواد المتعددة."
                            options = []
                    else:
                        s = "عذرًا، لم أتمكن من استخراج أسماء المواد من سؤالك."
                        options = []
                elif r[0] == ChatTask.ExamCourse:
                    response = self.CourseExam.handle_user_message(user_input)
                    if isinstance(response, str):
                        s = response
                        options = []
                    else:
                        s = "عذرًا، لم أتمكن من استخراج أسم المادة من سؤالك"
                        options = []
                elif r[0] == ChatTask.ExamDoc:
                    response = self.CourseExam.handle_user_message(user_input)
                    if isinstance(response, str):
                        s = response
                        options = []
                    else:
                        s = "عذرًا، لم أتمكن من استخراج أسم الدكتور من سؤالك"
                        options = []

                elif r[0] == ChatTask.UnknownTask:
                    s = choice(self.data.get("Unknown", ["لست متأكدًا من الإجابة على هذا."]))
                    options = []

        return s.strip(), options