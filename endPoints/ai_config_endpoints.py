import json
from flask import request, jsonify

json_file='Ai/ai_config.json'

def load_ai_config():
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise e


def get_ai_config():
    try:
        data = load_ai_config()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



def update_ai_config():
    try:
        data = request.json
        with open(json_file, 'r+', encoding='utf-8') as f:
            current_data = json.load(f)
            current_data.update(data)

            f.seek(0)
            json.dump(current_data, f, indent=2, ensure_ascii=False)
            f.truncate()
        return jsonify({"message": "Settings updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500