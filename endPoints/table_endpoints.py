import sqlite3
import os
from flask import jsonify, request
from Modules.helper_functions import uploaded_db_path

def get_tables(db_name):
    db_file = f"{db_name}.db"
    if not os.path.exists(db_file):
        return jsonify({"error": f"Database '{db_file}' does not exist."}), 404

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return jsonify(tables)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def create_table(db_name):
    if not request.is_json:
        return jsonify({"error": "Expected JSON format"}), 415

    data = request.get_json()
    table_name = data.get("name")

    if not table_name:
        return jsonify({"error": "Table name is required."}), 400

    if not table_name.replace("_", "").isalnum():
        return jsonify({"error": "Invalid table name."}), 400

    if not os.path.exists(uploaded_db_path):
        return jsonify({"error": f"Uploaded database does not exist."}), 404

    try:
        conn = sqlite3.connect(uploaded_db_path)
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS "{table_name}" (
                id INTEGER PRIMARY KEY AUTOINCREMENT
            );
        """)
        conn.commit()
        conn.close()
        return jsonify({"message": f"Table '{table_name}' created successfully in uploaded database."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_table(db_name):
    if not request.is_json:
        return jsonify({"error": "Expected JSON format"}), 415

    data = request.get_json()
    table_name = data.get("name")

    if not table_name:
        return jsonify({"error": "Table name is required."}), 400

    if not os.path.exists(uploaded_db_path):
        return jsonify({"error": f"Uploaded database does not exist."}), 404

    try:
        conn = sqlite3.connect(uploaded_db_path)
        cursor = conn.cursor()
        cursor.execute(f'DROP TABLE IF EXISTS "{table_name}"')
        conn.commit()
        conn.close()
        return jsonify({"message": f"Table '{table_name}' deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
