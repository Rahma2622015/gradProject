from Database.session import SessionLocal
from Database.DatabaseTabels.course import Course
from Database.DatabaseTabels.question import CourseQuestion

class CourseQuestionsAndAnswers:
    def __init__(self):
        self.session = SessionLocal()

    def get_course_questions(self, course_name: str, lang: str) :
        course = self.session.query(Course).filter(
            Course.name.ilike(f"%{course_name}%") |
            Course.short_name.ilike(f"%{course_name}%") |
            Course.code.ilike(f"%{course_name}%") |
            Course.name_arabic.ilike(f"%{course_name}%") |
            Course.short_name_arabic.ilike(f"%{course_name}%")
        ).first()

        if not course:
            return "Course not found." if lang == 'en' else "لم يتم العثور على المادة."

        if lang == 'ar':
            return [q for q in course.questions if q.question_arabic]
        else:
            return [q for q in course.questions if q.question]

    def get_all_questions_with_answers(self, question_id: int, lang: str ) -> list:
        question = self.session.query(CourseQuestion).filter(CourseQuestion.id == question_id).first()

        if not question:
            return ["Question not found." if lang == 'en' else "لم يتم العثور على السؤال."]

        if lang == 'ar' and not question.question_arabic:
            return ["لا يوجد نسخة عربية لهذا السؤال."]
        if lang == 'en' and not question.question:
            return ["No English version available for this question."]

        question_text = question.question_arabic if lang == 'ar' else question.question

        answers_data = [
            {
                'answer': ans.answer_arabic if lang == 'ar' else ans.answer,
                'score': ans.score
            }
            for ans in question.answers
            if (lang == 'ar' and ans.answer_arabic) or (lang == 'en' and ans.answer)
        ]

        return [{
            'question': question_text,
            'answers': answers_data
        }]