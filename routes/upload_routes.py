from flask import Blueprint
from endPoints.upload_endpoints import upload_sqlite

upload_blueprint = Blueprint('upload_blueprint', __name__)

upload_blueprint.route('/upload-sqlite', methods=['POST'])(upload_sqlite)
