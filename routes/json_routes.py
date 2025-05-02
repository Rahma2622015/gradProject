from flask import Blueprint
from endPoints.json_endpoints import list_json_files, save_config, get_json

json_blueprint = Blueprint('json_routes', __name__)

json_blueprint.route('/list_json_files', methods=['GET'])(list_json_files)
json_blueprint.route('/save_json/<path:filename>', methods=['POST'])(save_config)
json_blueprint.route('/get_json/<path:filename>', methods=['GET'])(get_json)
