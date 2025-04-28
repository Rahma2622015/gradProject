from Ai.EnglishAi.Datastorage_DB import DatabaseStorage
from Data.dataStorage import DataStorage

class ArRecommendationSystem:
    def __init__(self, data_storage: DatabaseStorage, memory: DataStorage):
        self.data_storage = data_storage
        self.memory = memory

    def start_recommendation(self, course_name):
        questions = self.data_storage.get_course_questions_arabic(course_name)
        if not questions or isinstance(questions, str):
            return "اسف لا يوجد اسئلة متاحة لهذا الكورس", []

        # Save course-related data in memory
        self.memory.save_data("course_name", course_name)
        self.memory.save_data("question_index", 0)
        self.memory.save_data("score", 0)
        self.memory.save_data("total_questions", len(questions))
        self.memory.save_data("question_ids", [q.id for q in questions])

        return self.ask_next_question()

    def ask_next_question(self):
        prev_data = self.memory.get_prev_data()
        question_index = prev_data.get("question_index")
        question_ids = prev_data.get("question_ids")

        if question_index >= len(question_ids):
            return self.generate_result()
        question_data = self.data_storage.get_question_with_answers_arabic(question_ids[question_index])
        if not question_data:
            return "خطا فى الوصول لمعلومات السؤال", []
        question_text = question_data["question"]
        answers = question_data["answers"]
        self.memory.save_data("current_answers", answers)
        choices = [ans["answer"] for ans in answers]
        return f"السؤال  {question_index + 1}: {question_text}", choices

    def receive_answer(self, user_answer: str):
        prev_data = self.memory.get_prev_data()
        answers = prev_data.get("current_answers")

        if not answers:
            return "يوجد خطا فى تنفيذ اجابتك , جرب مره اخرى", []
        normalized_input = user_answer.strip().lower()
        matched_answer = next(
            (ans for ans in answers if ans["answer"].strip().lower() == normalized_input),
            None
        )
        if not matched_answer:
            question_index = prev_data.get("question_index")
            question_text = self.data_storage.get_question_with_answers_arabic(prev_data["question_ids"][question_index])["question"]
            options = [ans["answer"] for ans in answers]
            return (
                f"اجابه خاطئة , ادخل الاجابة الصحيحه \n\n"
                f"السؤال  {question_index + 1}: {question_text}",
                options
            )

        selected_score = matched_answer["score"]
        current_score = prev_data.get("score", 0)
        updated_score = current_score + selected_score

        self.memory.save_data("score", updated_score)
        self.memory.save_data("question_index", prev_data.get("question_index") + 1)

        return self.ask_next_question()

    def generate_result(self):
        prev_data = self.memory.get_prev_data()
        total_score = prev_data.get("score", 0)
        question_ids = prev_data.get("question_ids", [])

        max_score = 0
        for q_id in question_ids:
            q_data = self.data_storage.get_question_with_answers_arabic(q_id)
            if q_data and "answers" in q_data:
                max_score += max(ans["score"] for ans in q_data["answers"])

        if max_score == 0:
            max_score = 1

        percentage = (total_score / max_score) * 100
        self.memory.clear_data()

        if percentage >= 70:
            return f"الاسكور {percentage:.2f}%. هذا الكورس مناسب لك انك تسجله .", []
        elif percentage >= 50:
            return f"الاسكور {percentage:.2f}%. تستطيع تسجيل هذا الكورس ولكن ربما تحتاج الى محهود اضافى حتى تحقق نتيجة جيدة.", []
        else:
            return f"الاسكور  {percentage:.2f}%. هذا الكورس غير مناسب لك , جرب تحسن من خبارتك حتى تتناسب مع تسجيله ", []
