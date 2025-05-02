import json
from flask import jsonify, request
import os
from Modules.helper_functions import uploaded_json_paths

BASE_DIR = os.path.abspath(r"E:\gradProject")

def list_json_files():
    try:
        all_json_files = []
        for root, dirs, files in os.walk(BASE_DIR):
            for f in files:
                if f.endswith(".json"):
                    relative_path = os.path.relpath(os.path.join(root, f), BASE_DIR)
                    all_json_files.append(relative_path.replace("\\", "/"))
                    uploaded_json_paths[relative_path.replace("\\", "/")] = os.path.join(root, f)
        return jsonify(all_json_files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_json(filename):
    try:
        filepath = os.path.join(BASE_DIR, filename)
        if not os.path.isfile(filepath):
            return jsonify({"message": "File not found"}), 404

        with open(filepath, "r", encoding="utf-8") as f:
            content = json.load(f)
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def save_config(filename):
    print("Received filename:", filename)
    print("Uploaded DB paths:", uploaded_json_paths)
    data = request.get_json()
    content = data.get("content")

    filepath = uploaded_json_paths.get(filename)
    if not filepath:
        return jsonify({"error": "File not found or not uploaded"}), 404

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        return jsonify({"message": "File saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500