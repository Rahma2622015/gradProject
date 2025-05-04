from flask import Blueprint
from endPoints.message_endpoints import messages

message_blueprint = Blueprint('message_routes', __name__)


message_blueprint.route('/messages', methods=['POST', 'GET'])(messages)
