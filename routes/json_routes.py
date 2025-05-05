from flask import Blueprint
from endPoints.json_endpoints import get_config, save_config, upload_json

json_blueprint = Blueprint('json_routes', __name__)

json_blueprint.route('/config/<filename>', methods=['GET'])(get_config)
json_blueprint.route('/save_json/<filename>', methods=['POST'])(save_config)
json_blueprint.route('/upload_json', methods=['POST'])(upload_json)
