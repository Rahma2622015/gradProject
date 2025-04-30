from flask import Blueprint
from endPoints.course_endpoints import get_courses, create_course, update_course, delete_course

course_blueprint = Blueprint('course_blueprint', __name__)

course_blueprint.route('/fetch', methods=['GET'])(get_courses)
course_blueprint.route('/courses', methods=['POST'])(create_course)
course_blueprint.route('/courses/<int:course_id>', methods=['PUT'])(update_course)
course_blueprint.route('/courses/<int:course_id>', methods=['DELETE'])(delete_course)
