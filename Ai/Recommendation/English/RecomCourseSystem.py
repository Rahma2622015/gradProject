from Database.Datastorage_DB import DatabaseStorage
from Modules.dataStorage import DataStorage
from Database.FetchDataCourses.QuestionsAndAnswers import CourseQuestionsAndAnswers

class RecommendationSystem:
    def __init__(self, data_storage: DatabaseStorage, memory: DataStorage,DS : CourseQuestionsAndAnswers):
        self.data_storage = data_storage
        self.memory = memory
        self.user_data = {}
        self.DSb = DS

    def start_recommendation(self, course_name, big_system=False):
        questions = self.DSb.get_course_questions(course_name, 'en')
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

        question_data_list = self.DSb.get_all_questions_with_answers(question_ids[question_index],'en')
        if not question_data_list or isinstance(question_data_list[0], str):
            return "Error retrieving question data.", []

        question_data = question_data_list[0]
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
            question_data_list = self.data_storage.courseQuestion.get_all_questions_with_answers(
                self.user_data["question_ids"][question_index], 'en')
            if not question_data_list or isinstance(question_data_list[0], str):
                return "Error retrieving question data.", []

            question_text = question_data_list[0]["question"]
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
            q_data_list = self.data_storage.courseQuestion.get_all_questions_with_answers(q_id,'en')
            if q_data_list and isinstance(q_data_list[0], dict) and "answers" in q_data_list[0]:
                max_score += max(ans["score"] for ans in q_data_list[0]["answers"])

        if max_score == 0:
            max_score = 1

        percentage = (total_score / max_score) * 100

        if big_system:
            return int(percentage)

        if percentage >= 70:
            result_text = (f"First of all, I am proud that you have reached "
                           f"this point and answered these questions. It is"
                           f" clear that you are very smart. As for the subject, "
                           f"it is very suitable for you to registe"
                           f"r based on your answers.")
        elif percentage >= 50:
            result_text = (f"First of all, I am proud that you have reached"
                           f" this point and answered these questions. It is clear"
                           f" that you are very smart. As for the subject, it is "
                           f"appropriate for you to register for it now,but you will "
                           f"need to put in some effort to excel in it based on your "
                           f"answers.")
        else:
            result_text = (f"First of all, I am proud that you have"
                           f" reached this point and answered these questions."
                           f" It is clear that you are very clever. As for the subject,"
                           f" unfortunately, it is not currently suitable for you to"
                           f" register for it now based on your answers, but do not"
                           f" worry at all about that. You will work on improving "
                           f"your experiences and register for it again. I trust you.")

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