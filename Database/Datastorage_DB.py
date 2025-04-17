from Database.database import SessionLocal, Course, Professor,CourseQuestion,Answers

class Data_Storage:
    def __init__(self):
        self.session = SessionLocal()

    def get_course_prerequisite(self, course_name: str):
        course = self.session.query(Course).filter(
            Course.name.ilike(f"%{course_name}%") |
            (Course.short_name.ilike(f"%{course_name}%")) |
            (Course.code.ilike(f"%{course_name}%"))
        ).first()

        if course:
            return [prerequisite.code for prerequisite in course.prerequisites]
        return None

    def get_course_description(self, course_name: str) -> str:
        course = self.session.query(Course).filter(
            Course.name.ilike(f"%{course_name}%") |
            (Course.short_name.ilike(f"%{course_name}%")) |
            (Course.code.ilike(f"%{course_name}%"))
        ).first()
        return course.description if course else "Course not found."

    def get_course_description_arabic(self, course_name: str) -> str:

        course = self.session.query(Course).filter(
            Course.name_arabic.ilike(f"%{course_name}%")).first()
        return course.description_arabic if course else "Course not found."


    def get_course_questions(self, course_name: str) -> list:
        course = self.session.query(Course).filter(
            Course.name.ilike(f"%{course_name}%") |
            (Course.short_name.ilike(f"%{course_name}%"))|
            (Course.code.ilike(f"%{course_name}%"))
        ).first()

        return course.questions if course else "Questions not found."

    def get_professor_info(self, professor_name: str) -> str:
        professor = self.session.query(Professor).filter(Professor.name.ilike(f"%{professor_name}%")).first()

        if not professor:
            return "Professor not found. Please check the spelling or try another name."

        return professor.description

    def get_professor_info_arabic(self, professor_name: str) -> str:
        professor = self.session.query(Professor).filter(Professor.name_arabic.ilike(f"%{professor_name}%")).first()

        if not professor:
            return "Professor not found. Please check the spelling or try another name."

        return professor.description_arabic

    def get_question_with_answers(self, question_id: int):
        question = self.session.query(CourseQuestion).filter(CourseQuestion.id == question_id).first()

        if not question:
            return None

        answers = self.session.query(Answers).filter(Answers.question_id == question_id).all()

        question_data = {
            'question': question.question,
            'answers': [{'answer': answer.answer, 'score': answer.score} for answer in answers]
        }

        return question_data
