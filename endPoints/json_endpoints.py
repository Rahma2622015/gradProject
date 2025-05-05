import json
from flask import jsonify, request
import os
from Modules.helper_functions import uploaded_db_path

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

def get_config(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            config_data = json.load(f)
        return jsonify(config_data), 200
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400


def save_config(filename):
    data = request.get_json()
    content = data.get("content")

    filepath = uploaded_db_path.get(filename)
    if not filepath:
        return jsonify({"error": "File not found or not uploaded"}), 404

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        return jsonify({"message": "File saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def upload_json():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if not file.filename.endswith('.json'):
        return jsonify({'error': 'Only .json files are supported'}), 400

    try:
        content = json.load(file)
        return jsonify({'content': content}), 200
    except Exception as e:
        return jsonify({'error': f'Invalid JSON format: {str(e)}'}), 400
