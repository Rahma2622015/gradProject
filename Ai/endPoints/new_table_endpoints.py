from flask import jsonify, request
from Modules.helper_functions import get_connection, close_connection

def get_table(db_name, table_name):
    try:
        conn, cur = get_connection(db_name)
        cur.execute(f"SELECT * FROM {table_name}")
        rows = [dict(row) for row in cur.fetchall()]
        columns = [col[0] for col in cur.description]
        return jsonify({"columns": columns, "rows": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

def add_row(db_name, table_name):
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        keys = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = list(data.values())
        conn, cur = get_connection(db_name)
        cur.execute(f"INSERT INTO {table_name} ({keys}) VALUES ({placeholders})", values)
        conn.commit()

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

def update_row(db_name, table_name):
    try:
        content = request.json
        old_row = content["oldRow"]
        new_row = content["newRow"]

        set_clause = ', '.join([f"{col} = ?" for col in new_row.keys()])
        where_clause = ' AND '.join([f"{col} = ?" for col in old_row.keys()])

        values = list(new_row.values()) + list(old_row.values())

        conn, cur = get_connection(db_name)
        cur.execute(f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}", values)
        conn.commit()
        return jsonify({"message": "Row updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

def delete_row(db_name, table_name):
    try:
        row = request.json
        where_clause = ' AND '.join([f"{col} = ?" for col in row.keys()])
        values = list(row.values())

        conn, cur = get_connection(db_name)
        cur.execute(f"DELETE FROM {table_name} WHERE {where_clause}", values)
        conn.commit()
        return jsonify({"message": "Row deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

def add_attribute(db_name, table_name):
    data = request.get_json()
    column_name = data.get("columnName")
    if not column_name:
        return jsonify({"error": "No column name provided"}), 400

    try:
        conn, cur = get_connection(db_name)

        cur.execute(f"PRAGMA table_info({table_name})")
        existing_columns = [column["name"] for column in cur.fetchall()]
        if column_name in existing_columns:
            return jsonify({"error": f"Column '{column_name}' already exists."}), 400

        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} TEXT;")
        close_connection(conn)

        return jsonify({"message": "Column added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
