import json
from random import choice
from Ai.Recommendation.RecommendationExamSystem import Recommendation
from Ai.EnglishAi.chattask import ChatTask
from Ai.Recommendation.RecomCourseSystem import RecommendationSystem
from Ai.EnglishAi.Tokeniztion import Tokenizers
from Ai.EnglishAi.Datastorage_DB import Data_Storage
from Data import DataStorage

import variables
class ReplyModuleRe:
    def __init__(self, json_path=variables.ResponseDataLocationRE):
        self.load_responses(json_path)
        self.recommender = Recommendation()
        self.course_dynamic_recommender = RecommendationSystem(Data_Storage(), DataStorage())
        self.tokenizer = Tokenizers()

    def load_responses(self, json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                self.data = json.load(file)
            print(f"[INFO] Response file loaded successfully: {json_path}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERROR] Failed to load response file: {e}")
            self.data = {}

    def generate_responseR(self, reply, user_input, user_id):
        s = ""
        options = []

        for r in reply:
            if isinstance(r, tuple) and len(r) > 0:
                if r[0] == ChatTask.ExamSystem:
                    response = self.recommender.handle_exam_recommendation(user_input, user_id)

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
                        # هنفترض إن course_name تم استخراجه من user_input مسبقًا
                        course_name = self.tokenizer.extract_course_name(user_input)
                        course_name = self.tokenizer.extract_course_name(user_input)
                        print(f"[INFO] Detected course name: {course_name}")  # فقط لأغراض التتبع
                        if course_name:
                            response = self.course_dynamic_recommender.start_recommendation(user_id, course_name)
                            if isinstance(response, str):
                                s = response
                                options = []  # ممكن تضيف options لو الأسئلة عندك في اختيارات
                            else:
                                print(f"[ERROR] Unexpected course recommendation format: {response}")
                                s = "Error processing course recommendation."
                                options = []
                        else:
                            s = "Sorry, I couldn't detect the course name from your question."
                            options = []
                elif r[0] == ChatTask.UnknownTask:
                    s = choice(self.data.get("Unknown", ["I'm not sure how to respond to that."]))
                    options = []

        return s.strip(), options
