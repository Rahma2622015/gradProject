from flask import Blueprint
from endPoints.professor_endpoints import get_professor, create_professor, update_professor, delete_professor

professor_blueprint = Blueprint('professor_routes', __name__)

professor_blueprint.route('/professor', methods=['GET'])(get_professor)
professor_blueprint.route('/professor', methods=['POST'])(create_professor)
professor_blueprint.route('/professor/<int:professor_id>', methods=['PUT'])(update_professor)
professor_blueprint.route('/professor/<int:professor_id>', methods=['DELETE'])(delete_professor)
