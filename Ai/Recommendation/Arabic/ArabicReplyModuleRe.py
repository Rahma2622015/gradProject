import json
from random import choice
from Ai.Recommendation.Arabic.ArabicRecomExamSystem import ArRecommendation
from Ai.EnglishAi.chattask import ChatTask
from Ai.Recommendation.Arabic.ArabicCoursesystem import ArRecommendationSystem
from Ai.EnglishAi.Tokeniztion import Tokenizers
from Ai.EnglishAi.Datastorage_DB import DatabaseStorage
from Data import DataStorage
from Ai.Recommendation.English.recommultiCourses import MultiCourseRecommendationSystem
import variables

data_storage = DatabaseStorage()
memory = DataStorage()

class ArReplyModuleRe:
    def __init__(self, json_path=variables.ArResponseDataLocationRE, memory_db=None, temp_storage=None):
        self.load_responses(json_path)
        self.recommender = ArRecommendation()
        self.course_dynamic_recommender = ArRecommendationSystem(memory_db, temp_storage)
        self.tokenizer = Tokenizers()
        # # self.course_selection_recommender = MultiCourseRecommendationSystem(
        # #     data_storage, memory, RecommendationSystem(memory_db, temp_storage)
        # # )

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

                elif r[0] == ChatTask.UnknownTask:
                    s = choice(self.data.get("Unknown", ["لست متاكد من الاجابة على هذا."]))
                    options = []

        return s.strip(), options
