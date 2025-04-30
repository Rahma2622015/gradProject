from flask import Blueprint
from endPoints.ai_config_endpoints import get_ai_config, update_ai_config

ai_config_blueprint = Blueprint('ai_config_routes', __name__)

ai_config_blueprint.route('/get_ai_config', methods=['GET'])(get_ai_config)
ai_config_blueprint.route('/update_ai_config', methods=['POST'])(update_ai_config)
