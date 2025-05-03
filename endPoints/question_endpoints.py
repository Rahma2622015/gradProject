from flask import jsonify, request
from Modules.helper_functions import get_uploaded_session
from Database.database import CourseQuestion

def get_question():
    try:
        session = get_uploaded_session()
        question_list = session.query(CourseQuestion).all()
        return jsonify([
            {
                "id": question.id,
                "question": question.question,
                "course_id": question.course_id,
                "question_arabic":question.question_arabic
            }
            for question in question_list
        ])
    except Exception as e:
        print("Error in get_question:", e)
        return jsonify({'error': str(e)}), 500

def create_question():
    session = get_uploaded_session()
    try:
        data = request.get_json()
        new_question = CourseQuestion(
            question=data['question'],
            course_id=data['course_id'],
            question_arabic=data['question_arabic']
        )
        session.add(new_question)
        session.commit()
        return jsonify({"message": "Question created successfully", "id": new_question.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

def update_question(question_id):
    session = get_uploaded_session()
    try:
        question_obj = session.query(CourseQuestion).get(question_id)
        if not question_obj:
            return jsonify({"error": "Question not found"}), 404
        data = request.get_json()
        question_obj.question = data.get('question', question_obj.question)
        question_obj.course_id = data.get('course_id', question_obj.course_id)
        question_obj.question_arabic=data.get('question_arabic',question_obj.question_arabic)
        session.commit()
        return jsonify({"message": "Question updated successfully"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

def delete_question(question_id):
    session = get_uploaded_session()
    try:
        question_obj = session.query(CourseQuestion).get(question_id)
        if not question_obj:
            return jsonify({"error": "Question not found"}), 404
        session.delete(question_obj)
        session.commit()
        return jsonify({"message": "Question deleted successfully"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
