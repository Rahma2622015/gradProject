from flask import Blueprint
from endPoints.course_professor_endpoints import  get_prof

course_professor_blueprint = Blueprint('course_professor_routes', __name__)

course_professor_blueprint.route('/prof', methods=['GET'])(get_prof)
