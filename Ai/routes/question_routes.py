from flask import Blueprint
from endPoints.question_endpoints import get_question, create_question, update_question, delete_question

question_blueprint = Blueprint('question_routes', __name__)

question_blueprint.route('/question', methods=['GET'])(get_question)
question_blueprint.route('/question', methods=['POST'])(create_question)
question_blueprint.route('/question/<int:question_id>', methods=['PUT'])(update_question)
question_blueprint.route('/question/<int:question_id>', methods=['DELETE'])(delete_question)
