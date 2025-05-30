import json
from random import choice
from Ai.Recommendation.English.RecommendationExamSystem import Recommendation
from Ai.EnglishAi.chattask import ChatTask
from Ai.Recommendation.English.RecomCourseSystem import RecommendationSystem
from Ai.EnglishAi.Tokeniztion import Tokenizers
from Database.Datastorage_DB import DatabaseStorage
from Modules import DataStorage
from Ai.Recommendation.English.recommultiCourses import MultiCourseRecommendationSystem
from Database.FetchDataCourses.QuestionsAndAnswers import CourseQuestionsAndAnswers
from Ai.Recommendation.English.examCourseSystem import SingleShotRecommendationSystem
from Database.FetchDataCourses.coureExamSystem import CourseSystem
from Database.FetchDataProfessors.professorExamSystem import ProfessorSystem
import variables

data_storage = DatabaseStorage()
memory = DataStorage()
dbs=CourseQuestionsAndAnswers()
dbcour=CourseSystem()
dbpro=ProfessorSystem()

class ReplyModuleRe:
    def __init__(self, json_path=variables.ResponseDataLocationRE):
        self.load_responses(json_path)

        self.recommender = Recommendation()
        self.course_dynamic_recommender = RecommendationSystem(data_storage, memory,dbs)
        self.tokenizer = Tokenizers()
        self.course_selection_recommender = MultiCourseRecommendationSystem(
            data_storage, memory, RecommendationSystem(data_storage, memory,dbs)
        )
        self.CourseExam=SingleShotRecommendationSystem(data_storage, memory,dbcour,dbpro)

    def load_responses(self, json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                self.data = json.load(file)
            print(f"[INFO] Response file loaded successfully: {json_path}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERROR] Failed to load response file: {e}")
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
                        s = "Error processing recommendation."
                        options = []

                elif r[0] == ChatTask.CourseSystem:
                    course_name = self.tokenizer.extract_course_name(user_input)
                    print(f"[INFO] Detected course name: {course_name}")
                    if course_name:
                        response = self.course_dynamic_recommender.start_recommendation(course_name)
                        if isinstance(response, str):
                            s = response
                            options = []
                        else:
                            print(f"[ERROR] Unexpected course recommendation format: {response}")
                            s = "Error processing course recommendation."
                            options = []
                    else:
                        s = "Sorry, I couldn't detect the course name from your question."
                        options = []
            elif r[0] == ChatTask.MultiCourseRecommendationTask:
                course_names = self.tokenizer.extract_all_course_names(user_input)
                print(f"[INFO] Detected course names: {course_names}")
                if course_names:
                    response, options = self.course_selection_recommender.start(course_names)
                    if isinstance(response, str):
                        s = response
                        options = []
                    else:
                        s = "Error processing multi-course recommendation."
                        options = []
                else:
                    s = "Sorry, I couldn't detect the course names from your question."
                    options = []

            elif r[0]==ChatTask.ExamCourse:
                response = self.CourseExam.handle_user_message(user_input)
                if isinstance(response, str):
                        s = response
                        options = []
                else:
                    s = "Sorry, I couldn't detect the course name from your question."
                    options = []
            elif r[0]==ChatTask.ExamDoc:
                response = self.CourseExam.handle_user_message(user_input)
                if isinstance(response, str):
                        s = response
                        options = []
                else:
                    s = "Sorry, I couldn't detect the doctor name from your question."
                    options = []
            elif r[0] == ChatTask.UnknownTask:
                    s = choice(self.data.get("Unknown", ["I'm not sure how to respond to that."]))
                    options = []

        return s.strip(), options