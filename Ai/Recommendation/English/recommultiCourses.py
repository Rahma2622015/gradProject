from Database.Datastorage_DB import DatabaseStorage
from Modules.dataStorage import DataStorage
from Ai.Recommendation.English.RecomCourseSystem import RecommendationSystem
from Ai.EnglishAi.Tokeniztion import Tokenizers

tokenizer = Tokenizers()

class MultiCourseRecommendationSystem:
    def __init__(self, data_storage:DatabaseStorage, memory:DataStorage, recommendation_system: RecommendationSystem):
         self.data_storage = data_storage
         self.memory = memory
         self.recommendation_system = recommendation_system

    def start(self, user_id, user_input):
        if isinstance(user_input, str):
            course_names = tokenizer.extract_all_course_names(user_input)
        elif isinstance(user_input, list):
            course_names = user_input
        else:
            return "Invalid input type. Please provide a list or a sentence.", []

        if not course_names:
            return "Sorry, I couldn't detect any valid course names from your message.", []

        self.memory.save_data(user_id, "all_courses", course_names)
        self.memory.save_data(user_id, "course_scores", {})
        self.memory.save_data(user_id, "current_course_index", 0)

        return self._start_next_course(user_id)

    def _start_next_course(self, user_id):
        course_list = self.memory.get_value(user_id, "all_courses")
        index =self.memory.get_value(user_id, "current_course_index")

        if index >= len(course_list):
            return self._finalize_recommendations(user_id)

        course_name = course_list[index]
        self.memory.save_data(user_id, "current_course", course_name)

        questions = self.recommendation_system.data_storage.get_course_questions(course_name)

        if not questions or isinstance(questions, str):
            current_scores = self.memory.get_value(user_id, "course_scores")
            current_scores[course_name] = 0
            self.memory.save_data(user_id, "course_scores", current_scores)
            self.memory.save_data(user_id, "current_course_index", index + 1)
            return self._start_next_course(user_id)

        self.memory.save_data(user_id, "question_index", 0)
        self.memory.save_data(user_id, "score", 0)
        self.memory.save_data(user_id, "total_questions", len(questions))
        self.memory.save_data(user_id, "question_ids", [q.id for q in questions])

        return self.ask_next_question(user_id)

    def ask_next_question(self, user_id):
        prev_data = self.memory.get_prev_data(user_id)
        question_index=self.memory.get_value(user_id,"question_index")
        #question_index = prev_data.get("question_index", 0)
        question_ids = prev_data.get("question_ids", [])
        course_name = prev_data.get("current_course", "")

        if question_index >= len(question_ids):
            return self._finish_course(user_id)

        # جلب بيانات السؤال الحالي
        question_data = self.data_storage.get_question_with_answers(question_ids[question_index])
        if not question_data:
            return "Error retrieving question data.", []

        # تحديث الأسئلة والاختيارات
        question_text = question_data["question"]
        answers = question_data["answers"]
        choices = [ans["answer"] for ans in answers]
        self.memory.save_data(user_id, "current_answers", answers)

        # عرض أول سؤال مع مقدمة
        if question_index == 0:
            intro_message = f"Now evaluating course: {course_name}\n"
            intro_message += f"Question 1: {question_text}"
            return intro_message, choices

        # عرض باقي الأسئلة
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
        question_index = prev_data.get("question_index")
        self.memory.save_data(user_id, "question_index", question_index + 1)
        self.memory.set_value(user_id, "question_index", question_index)

        if matched_answer:
            selected_score = matched_answer["score"]
            current_score = prev_data.get("score", 0)
            updated_score = current_score + selected_score
            self.memory.save_data(user_id, "score", updated_score)
            question_index+=1
            self.memory.set_value(user_id, "question_index", question_index)
            return self.ask_next_question(user_id)

        warning = "⚠️ Your answer didn't match any of the expected options. Moving to the next question.\n\n"
        next_q, choices = self.ask_next_question(user_id)
        return warning + next_q, choices

    def _finish_course(self, user_id):
        prev_data = self.memory.get_prev_data(user_id)
        total_score = prev_data.get("score", 0)
        question_ids = prev_data.get("question_ids", [])
        course_name = prev_data.get("current_course")

        max_score = 0
        for q_id in question_ids:
            q_data =self.data_storage.get_question_with_answers(q_id)
            if q_data and "answers" in q_data:
                max_score += max(ans["score"] for ans in q_data["answers"])

        if max_score == 0:
            max_score = 1

        percentage = (total_score / max_score) * 100
        scores =self.memory.get_value(user_id, "course_scores")
        scores[course_name] = percentage
        self.memory.save_data(user_id, "course_scores", scores)

        current_index =self.memory.get_value(user_id, "current_course_index")
        self.memory.save_data(user_id, "current_course_index", current_index + 1)

        return self._start_next_course(user_id)

    def _finalize_recommendations(self, user_id, top_n=3):
        scores =self.memory.get_value(user_id, "course_scores")
        sorted_courses = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_courses = sorted_courses[:top_n]

        self.memory.clear_data(user_id)

        result_text = "Based on your answers, the top recommended courses for you are:\n"
        for i, (course, score) in enumerate(top_courses, start=1):
            result_text += f"{i}. {course} ({score:.2f}%)\n"

        return result_text.strip(), []
