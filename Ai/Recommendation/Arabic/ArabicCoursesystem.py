from Database.Datastorage_DB import DatabaseStorage
from Modules.dataStorage import DataStorage
from Database.FetchDataCourses.QuestionsAndAnswers import CourseQuestionsAndAnswers

class ArRecommendationSystem:
    def __init__(self, data_storage: DatabaseStorage, memory: DataStorage,DS : CourseQuestionsAndAnswers):
        self.data_storage = data_storage
        self.DSb=DS
        self.memory = memory
        self.user_data = {}

    def start_recommendation(self, course_name, big_system=False):
        questions = self.DSb.get_course_questions(course_name, 'ar')
        if not questions or isinstance(questions, str):
            return "عذرًا، لم أتمكن من العثور على أي أسئلة لهذا الكورس.", []

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

        question_data_list = self.DSb.get_all_questions_with_answers(
            question_ids[question_index], 'ar')
        if not question_data_list or isinstance(question_data_list[0], str):
            return "حدث خطأ أثناء جلب بيانات السؤال.", []

        question_data = question_data_list[0]
        question_text = question_data["question"]
        answers = question_data["answers"]
        self.user_data["current_answers"] = answers
        choices = [ans["answer"] for ans in answers]

        return f"السؤال {question_index + 1}: {question_text}", choices

    def receive_answer(self, user_answer: str, big_system=False):
        answers = self.user_data.get("current_answers", [])
        if answers is None:
            print("خطأ: لا توجد إجابات محفوظة")
            return "حدث خطأ أثناء معالجة إجابتك. حاول مرة أخرى.", []

        normalized_input = user_answer.strip().casefold()
        matched_answer = next(
            (
                ans for ans in answers
                if ans["answer"].strip().casefold() == normalized_input
            ),
            None
        )

        if not matched_answer:
            question_index = self.user_data.get("question_index", 0)
            question_data_list = self.DSb.get_all_questions_with_answers(
                self.user_data["question_ids"][question_index], 'ar')
            if not question_data_list or isinstance(question_data_list[0], str):
                return "حدث خطأ أثناء جلب بيانات السؤال.", []

            question_text = question_data_list[0]["question"]
            options = [ans["answer"] for ans in answers]
            return (
                f"الإجابة غير صحيحة. من فضلك اختر إحدى الخيارات كما هي مكتوبة.\n\n"
                f"السؤال {question_index + 1}: {question_text}",
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
            print(f"النتيجة النهائية التي تم تخزينها: {final_score}")
            return None
        else:
            return re

    def generate_result(self, big_system=False):
        total_score = self.user_data.get("score", 0)
        question_ids = self.user_data.get("question_ids", [])

        max_score = 0
        for q_id in question_ids:
            q_data_list = self.DSb.get_all_questions_with_answers(q_id, 'ar')
            if q_data_list and isinstance(q_data_list[0], dict) and "answers" in q_data_list[0]:
                max_score += max(ans["score"] for ans in q_data_list[0]["answers"])

        if max_score == 0:
            max_score = 1

        percentage = (total_score / max_score) * 100

        if big_system:
            return int(percentage)

        if percentage >= 70:
            return (f"اول حاجه انا فخورة انك وصلت لهنا وجاوبت على الاسئلة ديه واضح انك شطور جدا اما بالنسبة للمادة"
                    f" فهى مناسبة لك تسجيلها جدا بناء على اجاباتك"), []
        elif percentage >= 50:
            return (f"اول حاجه انا فخورة انك وصلت لهنا وجاوبت على الاسئلة ديه واضح انك شطور جدا اما بالنسبة للمادة"
                    f" فهى مناسبة لك تسجيلها الان ولكن سوف تحتاج الى بذل بعض المجهود لتكون متفوق بها بناء على اجاباتك"), []
        else:
            return (f"اول حاجه انا فخورة انك وصلت لهنا وجاوبت على الاسئلة ديه واضح انك شطور جدا اما بالنسبة للمادة"
                    f" فهى للأسف حاليا مش مناسبة لك تسجيلها الان بناء على اجاباتك ولكن لا "
                    f"تقلق ابدا بشأن ذلك سوف تعمل على تحسين خبراتك وتعود تسجيلها انا واثقة بك"), []

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