import json
from random import choice
from Ai.Recommendation.RecommendationExamSystem import Recommendation
from Ai.Recommendation.RecomCourses import CourseRecommendation
from Ai.EnglishAi.ReplyTask import ReplyTask
import variables

class ReplyModuleRe:
    def __init__(self, json_path=variables.ResponseDataLocationRE
                 ,json_path2=variables.RecomLocation):
        self.load_responses(json_path)
        self.load_responses2(json_path2)
        self.recommender = Recommendation()
        self.course_recommender = CourseRecommendation()

    def load_responses(self, json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                self.general_data = json.load(file)
            print(f"[INFO] Response file loaded successfully: {json_path}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERROR] Failed to load response file: {e}")
            self.general_data = {}

    def load_responses2(self, json_path2):
        try:
            with open(json_path2, "r", encoding="utf-8") as file:
                self.recom_data = json.load(file)
            print(f"[INFO] Response file loaded successfully: {json_path2}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERROR] Failed to load response file: {e}")
            self.recom_data = {}

    def generate_responseR(self, reply, user_input, user_id):
        s = ""
        options = []

        for r in reply:
            if isinstance(r, tuple) and len(r) > 0:
                if r[0] == ReplyTask.ExamSystem:
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

                elif r[0] == ReplyTask.CourseSystem:
                    response = self.course_recommender.handle_course_recommendation(user_input, user_id)

                    if isinstance(response, tuple) and len(response) == 2:
                        s, options = response
                    elif isinstance(response, str):
                        s = response
                        options = []
                    else:
                        print(f"[ERROR] Unexpected response format: {response}")
                        s = "Error processing course recommendation."
                        options = []

                elif r[0] == ReplyTask.UnknownTask:
                    s = choice(self.general_data.get("Unknown", ["I'm not sure how to respond to that."]))
                    options = []

        return s.strip(), options
