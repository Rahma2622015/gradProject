from flask import Blueprint

from endPoints.table_endpoints import get_tables, create_table, delete_table

table_blueprint = Blueprint('table_routes', __name__)

table_blueprint.route('/get-tables/<db_name>', methods=['GET'])(get_tables)
table_blueprint.route('/create-table/<db_name>', methods=['POST'])(create_table)
table_blueprint.route('/delete-table/<db_name>', methods=['DELETE'])(delete_table)
