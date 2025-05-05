from flask import jsonify, request

from Modules.helper_functions import get_uploaded_session
from Database.DatabaseTabels.professor import Professor

def get_professor():
    try:
        session = get_uploaded_session()
        professor_list = session.query(Professor).all()
        return jsonify([
            {
                "id": professor.id,
                "name": professor.name,
                "description": professor.description,
                "name_arabic": professor.name_arabic,
                "description_arabic": professor.description_arabic,
            }
            for professor in professor_list
        ])
    except Exception as e:
        print("Error in get_professor:", e)
        return jsonify({'error': str(e)}), 500


def create_professor():
    session = get_uploaded_session()
    try:
        data = request.get_json()
        new_professor = Professor(
            name=data['name'],
            description=data['description'],
            name_arabic=data['name_arabic'],
            description_arabic=data['description_arabic']
        )
        session.add(new_professor)
        session.commit()
        return jsonify({"message": "Professor created successfully", "id": new_professor.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


def update_professor(professor_id):
    session = get_uploaded_session()
    try:
        professor_obj = session.query(Professor).get(professor_id)
        if not professor_obj:
            return jsonify({"error": "Professor not found"}), 404
        data = request.get_json()
        professor_obj.name = data.get('name', professor_obj.name)
        professor_obj.description = data.get('description', professor_obj.description)
        professor_obj.name_arabic = data.get('name_arabic', professor_obj.name_arabic)
        professor_obj.description_arabic = data.get('description_arabic', professor_obj.description_arabic)
        session.commit()
        return jsonify({"message": "Professor updated successfully"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


def delete_professor(professor_id):
    session = get_uploaded_session()
    try:
        professor_obj = session.query(Professor).get(professor_id)
        if not professor_obj:
            return jsonify({"error": "Professor not found"}), 404
        session.delete(professor_obj)
        session.commit()
        return jsonify({"message": "Professor deleted successfully"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
