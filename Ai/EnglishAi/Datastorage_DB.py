from Ai.EnglishAi.database import SessionLocal, Course, Professor,CourseQuestion,Answers

class Data_Storage:
    def __init__(self):
        self.session = SessionLocal()

    def get_course_description(self, course_name: str) -> str:
        session = SessionLocal()
        courses = session.query(Course).all()
        for c in courses:
            print(f"📚 {c.name} ({c.short_name}) → {c.description}")

        course = self.session.query(Course).filter(
            Course.name.ilike(f"%{course_name}%") |
            (Course.short_name.ilike(f"%{course_name}%"))
        ).first()
        print("4",course)
        return course.description if course else "Course not found."



    def get_course_questions(self, course_name: str) -> list:
        course = self.session.query(Course).filter(
            Course.name.ilike(f"%{course_name}%") |
            (Course.short_names.ilike(f"%{course_name}%"))
        ).first()

        return course.questions if course else "Questions not found."

    def get_professor_info(self, professor_name: str) -> str:
        professor = self.session.query(Professor).filter(Professor.name.ilike(f"%{professor_name}%")).first()

        if not professor:
            return "Professor not found. Please check the spelling or try another name."

        return professor.description

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
