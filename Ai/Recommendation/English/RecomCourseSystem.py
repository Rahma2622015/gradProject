from Ai.EnglishAi.Datastorage_DB import DatabaseStorage
from Data.dataStorage import DataStorage

class RecommendationSystem:
    def __init__(self, data_storage: DatabaseStorage, memory: DataStorage):
        self.data_storage = data_storage
        self.memory = memory

    def start_recommendation(self, user_id, course_name):
        questions = self.data_storage.get_course_questions(course_name)
        if not questions or isinstance(questions, str):
            return "Sorry, I couldn't find any questions for this course.", []

        self.memory.save_data(user_id, "course_name", course_name)
        self.memory.save_data(user_id, "question_index", 0)
        self.memory.save_data(user_id, "score", 0)
        self.memory.save_data(user_id, "total_questions", len(questions))
        self.memory.save_data(user_id, "question_ids", [q.id for q in questions])

        return self.ask_next_question(user_id)

    def ask_next_question(self, user_id):
        prev_data = self.memory.get_prev_data(user_id)
        question_index = prev_data.get("question_index")
        question_ids = prev_data.get("question_ids")

        if question_index >= len(question_ids):
            return self.generate_result(user_id)
        question_data = self.data_storage.get_question_with_answers(question_ids[question_index])
        if not question_data:
            return "Error retrieving question data.", []
        question_text = question_data["question"]
        answers = question_data["answers"]
        self.memory.save_data(user_id, "current_answers", answers)
        choices = [ans["answer"] for ans in answers]
        return f"Question {question_index + 1}: {question_text}", choices

    def receive_answer(self, user_id, user_answer: str):
        prev_data = self.memory.get_prev_data(user_id)
        answers = prev_data.get("current_answers")

        if not answers:
            return "There was an error processing your answer. Please try again.", []
        normalized_input = user_answer.strip().lower()
        matched_answer = next(
            (ans for ans in answers if ans["answer"].strip().lower() == normalized_input),
            None
        )
        if not matched_answer:
            question_index = prev_data.get("question_index")
            question_text = self.data_storage.get_question_with_answers(prev_data["question_ids"][question_index])[
                "question"]
            options = [ans["answer"] for ans in answers]
            return (
                f"Invalid answer. Please choose one of the options exactly as shown.\n\n"
                f"Question {question_index + 1}: {question_text}",
                options
            )

        selected_score = matched_answer["score"]
        current_score = prev_data.get("score", 0)
        updated_score = current_score + selected_score

        self.memory.save_data(user_id, "score", updated_score)
        self.memory.save_data(user_id, "question_index", prev_data.get("question_index") + 1)

        return self.ask_next_question(user_id)

    def generate_result(self, user_id):
        prev_data = self.memory.get_prev_data(user_id)
        total_score = prev_data.get("score", 0)
        question_ids = prev_data.get("question_ids", [])

        max_score = 0
        for q_id in question_ids:
            q_data = self.data_storage.get_question_with_answers(q_id)
            if q_data and "answers" in q_data:
                max_score += max(ans["score"] for ans in q_data["answers"])

        if max_score == 0:
            max_score = 1

        percentage = (total_score / max_score) * 100
        self.memory.clear_data(user_id)

        if percentage >= 70:
            return f"Your score is {percentage:.2f}%. This course is suitable for you to enroll.", []
        elif percentage >= 50:
            return f"Your score is {percentage:.2f}%. You can enroll in this course, but it may require extra effort.", []
        else:
            return f"Your score is {percentage:.2f}%. This course might not be suitable for you at the moment.", []