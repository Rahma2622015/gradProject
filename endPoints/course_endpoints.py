from flask import request, jsonify


from Database.DatabaseTabels.course import Course
from Modules.helper_functions import get_uploaded_session


def get_courses():
    try:
        session = get_uploaded_session()
        courses = session.query(Course).all()
        return jsonify([
            {
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "short_name": course.short_name,
                "code": course.code,
                "name_arabic": course.name_arabic,
                "description_arabic": course.description_arabic,
                "course_hours": course.course_hours,
                "course_degree": course.course_degree,
                "short_name_arabic": course.short_name_arabic,
                "department_id": course.department_id
            }
            for course in courses
        ])
    except Exception as e:
        print("Error in get_courses:", e)
        return jsonify({'error': str(e)}), 500


def create_course():
    session = get_uploaded_session()
    try:
        data = request.get_json()
        new_course = Course(
            name=data['name'],
            description=data['description'],
            short_name=data.get('short_name'),
            code=data['code'],
            name_arabic=data['name_arabic'],
            description_arabic=data['description_arabic'],
            course_hours=data['course_hours'],
            course_degree=data['course_degree'],
            short_name_arabic=data['short_name_arabic'],
            department_id=data['department_id']
        )
        session.add(new_course)
        session.commit()
        return jsonify({"message": "Course created successfully", "id": new_course.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


def update_course(course_id):
    session = get_uploaded_session()
    try:
        course = session.query(Course).get(course_id)
        if not course:
            return jsonify({"error": "Course not found"}), 404
        data = request.get_json()
        course.name = data.get('name', course.name)
        course.description = data.get('description', course.description)
        course.short_name = data.get('short_name', course.short_name)
        course.code = data.get('code', course.code)
        course.name_arabic = data.get('name_arabic', course.name_arabic)
        course.description_arabic = data.get('description_arabic', course.description_arabic)
        course.course_hours = data.get('course_hours', course.course_hours)
        course.course_degree = data.get('course_degree', course.course_degree)
        course.short_name_arabic = data.get('short_name_arabic', course.short_name_arabic)
        course.department_id = data.get('department_id', course.department_id)
        session.commit()
        return jsonify({"message": "Course updated successfully"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


def delete_course(course_id):
    session = get_uploaded_session()
    try:
        course = session.query(Course).get(course_id)
        if not course:
            return jsonify({"error": "Course not found"}), 404
        session.delete(course)
        session.commit()
        return jsonify({"message": "Course deleted successfully"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
