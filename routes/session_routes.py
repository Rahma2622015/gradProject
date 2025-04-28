from flask import Blueprint
from endPoints.session_endpoints import start_session, close_session

session_blueprint = Blueprint('session_routes', __name__)

session_blueprint.route('/start-session', methods=['POST'])(start_session)
session_blueprint.route('/close-session', methods=['POST'])(close_session)
