from flask import Blueprint
from endPoints.prerequisite_endpoints import get_pre

prerequisite_blueprint = Blueprint('prerequisite_routes', __name__)

prerequisite_blueprint.route('/pre', methods=['GET'])(get_pre)
