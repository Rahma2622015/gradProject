from flask import Blueprint
from endPoints.new_table_endpoints import get_table, add_row, update_row, delete_row, add_attribute

new_table_blueprint = Blueprint('new_table_routes', __name__)


new_table_blueprint.route("/get-table/<db_name>/<table_name>", methods=["GET"])(get_table)
new_table_blueprint.route("/add-row/<db_name>/<table_name>", methods=["POST"])(add_row)
new_table_blueprint.route("/update-row/<db_name>/<table_name>", methods=["POST"])(update_row)
new_table_blueprint.route("/delete-row/<db_name>/<table_name>", methods=["POST"])(delete_row)
new_table_blueprint.route("/add-attribute/<db_name>/<table_name>", methods=["POST"])(add_attribute)
