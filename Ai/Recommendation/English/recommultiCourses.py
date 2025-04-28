from Ai.EnglishAi.Datastorage_DB import DatabaseStorage
from Data.dataStorage import DataStorage
from Ai.Recommendation.English.RecomCourseSystem import RecommendationSystem
from Ai.EnglishAi.Tokeniztion import Tokenizers
from Ai.EnglishAi.Preprocessing import Preprocessors

tokenizer = Tokenizers()
pre = Preprocessors()

class MultiCourseRecommendationSystem:
    def __init__(self, data_storage: DatabaseStorage, memory: DataStorage, recommendation_system: RecommendationSystem):
        self.data_storage = data_storage
        self.memory = memory
        self.recommendation_system = recommendation_system
        self.user_data = {}

    def start(self, user_input):
        if isinstance(user_input, str):
            course_names = tokenizer.extract_all_course_names(user_input)
            self.user_data["initial_message"] = user_input
        elif isinstance(user_input, list):
            course_names = user_input
        else:
            return "Invalid input type. Please provide a list or a sentence.", []

        if not course_names:
            return "Sorry, I couldn't detect any valid course names from your message.", []

        self.user_data["all_courses"] = course_names
        self.user_data["course_scores"] = {}
        self.user_data["current_course_index"] = 0

        return self._start_next_course()

    def handle_answer(self, user_input):
        course_name = self.user_data.get("current_course")

        if course_name is None:
            return "No current course data found.", []

        result = self.recommendation_system.continue_recommendation(user_input, True)

        if isinstance(result, tuple) and len(result) == 2:
            response, options = result
        else:
            # لو النتيجة عبارة عن سكور فقط، خزنه وخلاص بدون ما ترجعه للمستخدم
            score = result if isinstance(result, (int, float)) else 0

            current_scores = self.user_data.get("course_scores", {})
            current_scores[course_name] = score
            self.user_data["course_scores"] = current_scores

            self.user_data["current_course_index"] += 1

            return self._start_next_course()

        if isinstance(result, (int, float)):
            score = result

            current_scores = self.user_data.get("course_scores", {})
            current_scores[course_name] = score if score is not None else 0
            self.user_data["course_scores"] = current_scores

            self.user_data["current_course_index"] += 1

            return self._start_next_course()

        return response, options

    def _start_next_course(self):
        course_list = self.user_data.get("all_courses")
        index = self.user_data.get("current_course_index")

        if index >= len(course_list):
            return self._finalize_recommendations()

        course_name = course_list[index]
        self.user_data["current_course"] = course_name

        result = self.recommendation_system.start_recommendation(course_name, True)

        if isinstance(result, tuple) and len(result) == 2:
            response, options = result
        else:
            response = result
            options = []

        return f"For the course {course_name}, the first question is:\n{response}", options

    def _finalize_recommendations(self):
        pre = Preprocessors()
        initial_message = self.user_data.get("initial_message")

        if initial_message:
            tokens = tokenizer.tokenize(initial_message)
            pos_tags = tokenizer.pos_tag(tokens)
            top_n = pre.extract_first_number(tokens, pos_tags)
        else:
            top_n = None

        if top_n is None:
            top_n = 3

        scores = self.user_data.get("course_scores", {})
        sorted_courses = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_courses = sorted_courses[:top_n]

        self.user_data.clear()

        result_text = "Based on your answers, the top recommended courses for you are:\n"
        for i, (course, score) in enumerate(top_courses, start=1):
            result_text += f"{i}. {course} ({score:.2f}%)\n"

        return result_text.strip(), []
