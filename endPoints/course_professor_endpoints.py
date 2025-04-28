from flask import jsonify
from Modules.helper_functions import get_uploaded_session
from Database.database import course_professor

def get_prof():
    try:
        session = get_uploaded_session()
        prof_obj = session.query(course_professor).all()
        return jsonify([
            {
                "course_id": prof.course_id,
                "professor_id": prof.professor_id,
            }
            for prof in prof_obj
        ])
    except Exception as e:
        print("Error in get_prof:", e)
        return jsonify({'error': str(e)}), 500
