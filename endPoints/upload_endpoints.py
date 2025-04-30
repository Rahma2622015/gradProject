from flask import request, jsonify
from werkzeug.utils import secure_filename
from Modules.helper_functions import allowed_file
import os

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))

def upload_sqlite():
    global uploaded_db_path

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        uploaded_db_path = filepath
        return jsonify({"message": "File uploaded successfully"})

    return jsonify({"error": "Invalid file format"}), 400
