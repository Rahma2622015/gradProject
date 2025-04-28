from flask import jsonify
from Modules.helper_functions import get_uploaded_session
from Database.database import course_prerequisites

def get_pre():
    try:
        session = get_uploaded_session()
        pre_obj = session.query(course_prerequisites).all()
        return jsonify([
            {
                "course_id": pre.course_id,
                "prerequisite_id": pre.prerequisite_id,
            }
            for pre in pre_obj
        ])
    except Exception as e:
        print("Error in get_pre:", e)
        return jsonify({'error': str(e)}), 500
