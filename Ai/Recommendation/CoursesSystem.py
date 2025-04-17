from Ai.EnglishAi.Datastorage_DB import Data_Storage
from Data.dataStorage import DataStorage
from Ai.Recommendation.RecomCourseSystem import RecommendationSystem
from Ai.EnglishAi.Tokeniztion import Tokenizers

class CourseSelectionRecommendationSystem:
    def __init__(self, data_storage: Data_Storage, memory: DataStorage, recommender: RecommendationSystem, text_processor: Tokenizers):
        self.data_storage = data_storage
        self.memory = memory
        self.recommender = recommender
        self.text_processor = text_processor

    def start(self, user_id, user_input, top_n=3):
        course_names = self.text_processor.extract_all_course_names(user_input)
        if not course_names:
            return "No valid course names were detected. Please try again.", []

        self.memory.save_data(user_id, "selected_courses", course_names)
        self.memory.save_data(user_id, "top_n", top_n)
        self.memory.save_data(user_id, "current_stage", "ask_gpa")

        return "What is your GPA?", ["Greater than 2", "Equal to 2", "Less than 2"]

    def receive_gpa(self, user_id, gpa_response):
        self.memory.save_data(user_id, "gpa", gpa_response)
        self.memory.save_data(user_id, "course_scores", {})
        self.memory.save_data(user_id, "current_course_index", 0)
        return self.ask_next_course_question(user_id)

    def ask_next_course_question(self, user_id):
        prev = self.memory.get_prev_data(user_id)
        courses = prev.get("selected_courses", [])
        index = prev.get("current_course_index", 0)

        if index >= len(courses):
            return self.show_top_recommendations(user_id)

        course_name = courses[index]
        message, choices = self.recommender.start_recommendation(user_id + f"_{course_name}", course_name)
        self.memory.save_data(user_id, "current_course", course_name)

        gpa_msg = ""
        gpa = prev.get("gpa")
        if gpa == "Less than 2":
            gpa_msg = f"⚠️ Your GPA is below 2. It's recommended to select courses that may help boost it. Let's evaluate **{course_name}**."
        elif gpa == "Equal to 2":
            gpa_msg = f"🔔 Your GPA is 2. You need to stay focused. Let's evaluate **{course_name}**."
        else:
            gpa_msg = f"✅ Great! Let's evaluate **{course_name}**."

        return f"{gpa_msg}\n\n{message}", choices

    def receive_course_answer(self, user_id, user_answer):
        prev = self.memory.get_prev_data(user_id)
        current_course = prev.get("current_course")
        modified_id = user_id + f"_{current_course}"
        message, choices = self.recommender.receive_answer(modified_id, user_answer)

        # Check if the message contains a valid score percentage
        if isinstance(message, str) and "score" in message.lower():
            try:
                # Extract percentage and ensure it's valid
                percentage = float(message.split("%")[-2].split()[-1])
            except (ValueError, IndexError):
                percentage = 0.0  # Default to 0 if conversion fails

            course_scores = prev.get("course_scores", {})
            course_scores[current_course] = percentage
            self.memory.save_data(user_id, "course_scores", course_scores)

            current_index = prev.get("current_course_index", 0)
            self.memory.save_data(user_id, "current_course_index", current_index + 1)

            return self.ask_next_course_question(user_id)

        # If message doesn't contain a valid score, handle accordingly
        return message, choices

    def show_top_recommendations(self, user_id):
        prev = self.memory.get_prev_data(user_id)
        scores = prev.get("course_scores", {})
        top_n = prev.get("top_n", 3)

        sorted_courses = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_courses = sorted_courses[:top_n]

        msg = f"\U0001F50D Based on your answers, here are your top {top_n} recommended courses:\n"
        for i, (course, score) in enumerate(top_courses, 1):
            msg += f"{i}. {course} - {score:.2f}%\n"

        self.memory.clear_data(user_id)
        return msg, []
