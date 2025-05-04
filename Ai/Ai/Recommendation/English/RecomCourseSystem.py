from Database.Datastorage_DB import DatabaseStorage
from Modules.dataStorage import DataStorage

class RecommendationSystem:
    def __init__(self, data_storage: DatabaseStorage, memory: DataStorage):
        self.data_storage = data_storage
        self.memory = memory
        self.user_data = {}

    def start_recommendation(self, course_name, big_system=False):
        questions = self.data_storage.courseQuestion.get_course_questions(course_name)
        if not questions or isinstance(questions, str):
            return "Sorry, I couldn't find any questions for this course.", []

        self.user_data = {
            "course_name": course_name,
            "question_index": 0,
            "score": 0,
            "total_questions": len(questions),
            "question_ids": [q.id for q in questions]
        }

        return self.ask_next_question(big_system)

    def ask_next_question(self, big_system=False):
        question_index = self.user_data.get("question_index", 0)
        question_ids = self.user_data.get("question_ids", [])

        if question_index >= len(question_ids):
            result = self.generate_result(big_system)

            if big_system and isinstance(result, (int, float)):
                self.user_data["final_score"] = result
                return None

            return result

        question_data = self.data_storage.courseQuestion.get_all_questions_with_answers(question_ids[question_index],'en')
        if not question_data:
            return "Error retrieving question data.", []

        question_text = question_data["question"]
        answers = question_data["answers"]
        self.user_data["current_answers"] = answers
        choices = [ans["answer"] for ans in answers]

        return f"Question {question_index + 1}: {question_text}", choices

    def receive_answer(self, user_answer: str, big_system=False):
        answers = self.user_data.get("current_answers", [])
        if answers is None:
            print("Error: answers is None")
            return "There was an error processing your answer. Please try again.", []

        normalized_input = user_answer.strip().lower()
        matched_answer = next(
            (ans for ans in answers if ans["answer"].strip().lower() == normalized_input),
            None
        )

        if not matched_answer:
            question_index = self.user_data.get("question_index", 0)
            question_text = self.data_storage.courseQuestion.get_question_with_answers(self.user_data["question_ids"][question_index],'en')["question"]
            options = [ans["answer"] for ans in answers]
            return (
                f"Invalid answer. Please choose one of the options exactly as shown.\n\n"
                f"Question {question_index + 1}: {question_text}",
                options
            )

        selected_score = matched_answer.get("score", 0)
        current_score = self.user_data.get("score", 0)
        updated_score = current_score + selected_score

        self.user_data["score"] = updated_score
        self.user_data["question_index"] = self.user_data.get("question_index", 0) + 1

        re = self.ask_next_question(big_system)

        if re is None and big_system:
            final_score = self.user_data.get("final_score")
            print(f"Final score stored: {final_score}")
            return None
        else:
            return re

    def generate_result(self, big_system=False):
        total_score = self.user_data.get("score", 0)
        question_ids = self.user_data.get("question_ids", [])

        max_score = 0
        for q_id in question_ids:
            q_data = self.data_storage.courseQuestion.get_question_with_answers(q_id,'en')
            if q_data and "answers" in q_data:
                max_score += max(ans["score"] for ans in q_data["answers"])

        if max_score == 0:
            max_score = 1

        percentage = (total_score / max_score) * 100

        if big_system:
            return int(percentage)

        if percentage >= 70:
            result_text = f"Your score is {percentage:.2f}%. This course is suitable for you to enroll."
        elif percentage >= 50:
            result_text = f"Your score is {percentage:.2f}%. You can enroll in this course, but it may require extra effort."
        else:
            result_text = f"Your score is {percentage:.2f}%. This course might not be suitable for you at the moment."

        return result_text, []

    def continue_recommendation(self, user_answer: str, big_system=False):
        result = self.receive_answer(user_answer, big_system)

        if result is None and big_system:
            return None

        if isinstance(result, tuple) and len(result) == 2:
            return result

        return result, []

    def get_final_score(self):
        return self.user_data.get("final_score")

    def clear_user_data(self):
        self.user_data.clear()
