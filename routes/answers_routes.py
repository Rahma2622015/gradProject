from flask import Blueprint
from endPoints.answers_endpoints import get_answers, create_answer, update_answer, delete_answer

answers_blueprint = Blueprint('answers_routes', __name__)

answers_blueprint.route('/answer', methods=['GET'])(get_answers)
answers_blueprint.route('/answers', methods=['POST'])(create_answer)
answers_blueprint.route('/answers/<int:answer_id>', methods=['PUT'])(update_answer)
answers_blueprint.route('/answers/<int:answer_id>', methods=['DELETE'])(delete_answer)
