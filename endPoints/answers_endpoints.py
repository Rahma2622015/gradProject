from flask import jsonify, request

from Database.database import Answers
from Modules.helper_functions import get_uploaded_session


def get_answers():
    try:
        session = get_uploaded_session()
        answer_list = session.query(Answers).all()
        return jsonify([
            {
                "id": answer.id,
                "answer": answer.answer,
                "score": answer.score,
                "question_id": answer.question_id,
                "answer_arabic": answer.answer_arabic,
                "question": answer.question
            }
            for answer in answer_list
        ])
    except Exception as e:
        print("Error in get_answer:", e)
        return jsonify({'error': str(e)}), 500


def create_answer():
    session = get_uploaded_session()
    try:
        data = request.get_json()
        new_answer = Answers(
            answer=data['answer'],
            score=data['score'],
            question_id=data.get('question_id'),
            answer_arabic=data.get('answer_arabic'),
            question=data.get('question')
        )
        session.add(new_answer)
        session.commit()
        return jsonify({"message": "Answer created successfully", "id": new_answer.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


def update_answer(answer_id):
    session = get_uploaded_session()
    try:
        answer_obj = session.query(Answers).get(answer_id)
        if not answer_obj:
            return jsonify({"error": "Answer not found"}), 404
        data = request.get_json()
        answer_obj.answer = data.get('answer', answer_obj.answer)
        answer_obj.score = data.get('score', answer_obj.score)
        answer_obj.question_id = data.get('question_id', answer_obj.question_id)
        answer_obj.answer_arabic = data.get('answer_arabic', answer_obj.answer_arabic)
        answer_obj.question = data.get('question', answer_obj.question)
        session.commit()
        return jsonify({"message": "Answer updated successfully"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


def delete_answer(answer_id):
    session = get_uploaded_session()
    try:
        answer = session.query(Answers).get(answer_id)
        if not answer:
            return jsonify({"error": "Answer not found"}), 404
        session.delete(answer)
        session.commit()
        return jsonify({"message": "Answer deleted successfully"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
