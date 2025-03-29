import json
from random import choice
from Ai.Recommendation.RecommendationExamSystem import Recommendation
from Ai.EnglishAi.ReplyTask import ReplyTask
import variables
class ReplyModuleRe:
    def __init__(self, json_path=variables.ResponseDataLocationRE):
        self.load_responses(json_path)
        self.recommender = Recommendation()

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

                elif r[0] == ReplyTask.UnknownTask:
                    s = choice(self.data.get("Unknown", ["I'm not sure how to respond to that."]))
                    options = []

        return s.strip(), options
