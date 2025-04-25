import os
import json
import random
import sqlite3
from Data.class_client import Client
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from Ai.RecivingFunction import receive
from gevent.pywsgi import WSGIServer
import variables
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Ai.EnglishAi.database import Course, Answers, CourseQuestion, course_professor,Professor , course_prerequisites
from werkzeug.utils import secure_filename

chat_bot = Flask(__name__)
data_file='session_data.json'
client_list=[]
chat_bot.secret_key = os.urandom(24)
uploaded_db_path = "university_information.db"
CORS(chat_bot)
BASE_DIR = os.path.abspath(r"D:\project_grid")
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
chat_bot.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_uploaded_session():
    global uploaded_db_path
    if not uploaded_db_path or not os.path.exists(uploaded_db_path):
        raise Exception("No database uploaded or file not found")

    engine = create_engine(f"sqlite:///{uploaded_db_path}")
    Session = sessionmaker(bind=engine)
    return Session()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'db', 'sqlite'}

def load_data():
    if not os.path.exists(data_file):
        return {}
    try:
        with open(data_file, 'r') as file:
            data = json.load(file)
            if not isinstance(data, dict):
                raise ValueError("Data is not in the correct format!")
            return data
    except (json.JSONDecodeError, ValueError) as e:
        return {}


def save_data(data):
    with open(data_file, 'w') as file:
        json.dump(data, file)


def remove_data(client_id):
    try:
        client_data = load_data()
        if str(client_id) in client_data:
            del client_data[str(client_id)]
            save_data(client_data)
    except Exception as e:
        print(f"Error removing data item: {e}")


def generateClientId():
    new_id = random.randint(1, 999999)
    client_data = load_data()
    while str(new_id) in client_data:
        new_id = random.randint(1, 999999)
    return new_id


def get_client_by_id(id):
    id = int(id)
    for c in client_list:
        if c.id == id:
            return c
    return None


@chat_bot.route('/start-session', methods=['POST'])
def start_session():
    try:
        client = Client()
        client_id = generateClientId()
        client_data = load_data()

        client_data[str(client_id)] = {
            'id': client_id,
            'session_started': True
        }
        save_data(client_data)

        session['client_id'] = client_id

        client_list.append(client)

        for c in client_list:
            if c.endSession():
                client_list.remove(c)
                remove_data(c.id)

        if client.startSession(client_id):
            return jsonify({"message": "Session started", "client_id": client_id})
        else:
            return jsonify({"error": "Failed to start session"}), 500

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

@chat_bot.route('/close-session', methods=['POST'])
def close_session():
    try:
        data = request.get_json()
        client_id = data.get('client_id')

        if not client_id:
            return jsonify({"error": "Client ID is missing!"}), 400

        client_to_remove = get_client_by_id(client_id)

        if client_to_remove:
            remove_data(client_id)
            client_list.remove(client_to_remove)
            return jsonify({"message": "Session closed", "client_id": client_id})
        else:
            return jsonify({"error": "Client ID not found!"}), 404

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@chat_bot.route('/messages', methods=['POST', 'GET'])
def messages():
    try:
        message = request.get_json()
        user_message = message.get('userMessage', '')
        client_id = message.get('id', '')
        client = get_client_by_id(client_id)

        if not client:
            return jsonify({"error": "Please start new session!"}), 404  # Not Found
        if not user_message:
            return jsonify({"error": "Message is required"}), 400  # Bad Request
        if not client_id:
            return jsonify({"error": "Client ID is required"}), 400  # Bad Request

        try:
            reply_text, reply_list, _ = receive(user_message, client.data, client_id)

            for c in client_list:
                if c.endSession():
                    client_list.remove(c)
                    remove_data(c.id)

            return jsonify({"reply": reply_text, "list": reply_list})

        except Exception as ex:
            return jsonify({"error": f"Error in receiving reply: {str(ex)}"})


    except Exception as e:
        return jsonify({"error":f"Error in send :{str(e)}"})
#course
@chat_bot.route('/fetch', methods=['GET'])
def get_courses():
    try:
        session = get_uploaded_session()
        courses = session.query(Course).all()
        return jsonify([
            {
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "short_name": course.short_name,
                "code": course.code,
                "name_arabic":course.name_arabic,
                "description_arabic":course.description_arabic,
                "course_hours":course.course_hours,
                "course_degree":course.course_degree
            }
            for course in courses
        ])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@chat_bot.route('/courses', methods=['POST'])
def create_course():
    session = get_uploaded_session()
    try:
        data = request.get_json()
        new_course = Course(
            name=data['name'],
            description=data['description'],
            short_name=data.get('short_name'),
            code=data['code'],
            name_arabic=['name_arabic'],
            description_arabic=['description_arabic'] ,
            course_hours=['course_hours'],
            course_degree=['course_degree']
        )
        session.add(new_course)
        session.commit()
        return jsonify({"message": "Course created successfully", "id": new_course.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@chat_bot.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    session = get_uploaded_session()
    try:
        course = session.query(Course).get(course_id)
        if not course:
            return jsonify({"error": "Course not found"}), 404
        data = request.get_json()
        course.name = data.get('name', course.name)
        course.description = data.get('description', course.description)
        course.short_name = data.get('short_name', course.short_name)
        course.code = data.get('code', course.code)
        course.name_arabic = data.get('name_arabic', course.name_arabic)
        course.description_arabic = data.get('description_arabic', course.description_arabic)
        course.course_hours = data.get('course_hours', course.course_hours)
        course.course_degree=data.get('course_degree',course.course_degree)
        session.commit()
        return jsonify({"message": "Course updated successfully"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@chat_bot.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    session = get_uploaded_session()
    try:
        course = session.query(Course).get(course_id)
        if not course:
            return jsonify({"error": "Course not found"}), 404
        session.delete(course)
        session.commit()
        return jsonify({"message": "Course deleted successfully"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@chat_bot.route('/upload-sqlite', methods=['POST'])
def upload_sqlite():
    global uploaded_db_path

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(chat_bot.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        uploaded_db_path = filepath
        return jsonify({"message": "File uploaded successfully"})

    return jsonify({"error": "Invalid file format"}), 400
#Answer
@chat_bot.route('/answers', methods=['GET'])
def get_answers():
    try:
        session = get_uploaded_session()
        answer_list = session.query(Answers).all()
        return jsonify([
            {
                "id": answer.id,
                "answer": answer.answer,
                "score": answer.score,
                "question_id": answer.question_id,
                "answer_arabic":answer.answer_arabic
            }
            for answer in answer_list
        ])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@chat_bot.route('/answers', methods=['POST'])
def create_answer():
    session = get_uploaded_session()
    try:
        data = request.get_json()
        new_Answer = Answers(
            answer=data['answer'],
            score=data['score'],
            question_id=data.get('question_id'),
            answer_arabic=data.get('answer_arabic'),
        )
        session.add(new_Answer)
        session.commit()
        return jsonify({"message": "Answer  created successfully", "id": new_Answer.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@chat_bot.route('/answers/<int:answer_id>', methods=['PUT'])
def update_answer(answer_id):
    session = get_uploaded_session()
    try:
        answer_obj = session.query(Answers).get(answer_id)
        if not answer_obj:
            return jsonify({"error": "Answer not found"}), 404
        data = request.get_json()
        answer_obj.answer = data.get('answer', answer_obj.answer)
        answer_obj.score = data.get('score', answer_obj.score)
        answer_obj.question_id = data.get('question_id', answer_obj.question_id)
        answer_obj.answer_arabic = data.get('answer_arabic', answer_obj.answer_arabic)
        session.commit()
        return jsonify({"message": "Answer updated successfully"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@chat_bot.route('/answers/<int:answer_id>', methods=['DELETE'])
def delete_Answer(answer_id):
    session = get_uploaded_session()
    try:
        answer = session.query(Answers).get(answer_id)
        if not answer:
            return jsonify({"error": "Answer not found"}), 404
        session.delete(answer)
        session.commit()
        return jsonify({"message": "Answer deleted successfully"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
#prof
@chat_bot.route('/professor', methods=['GET'])
def get_professor():
    try:
        session = get_uploaded_session()
        professor_list = session.query(Professor).all()
        return jsonify([
            {
                "id": professor.id,
                "name": professor.name,
                "description": professor.description,
                "name_arabic": professor.name_arabic,
                "description_arabic": professor.description_arabic,
            }
            for professor in professor_list
        ])
    except Exception as e:
        print("Error in get_professor:", e)
        return jsonify({'error': str(e)}), 500
@chat_bot.route('/professor', methods=['POST'])
def create_professor():
    session = get_uploaded_session()
    try:
        data = request.get_json()
        new_professor = Professor(
            name=data['name'],
            description=data['description'],
            name_arabic=data['name_arabic'],
            description_arabic=data['description_arabic'],
        )
        session.add(new_professor)
        session.commit()
        return jsonify({"message": "professor  created successfully", "id": new_professor.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@chat_bot.route('/professor/<int:professor_id>', methods=['PUT'])
def update_professor(professor_id):
    session = get_uploaded_session()
    try:
        professor_obj = session.query(Professor).get(professor_id)
        if not professor_obj:
            return jsonify({"error": "professor not found"}), 404
        data = request.get_json()
        professor_obj.name = data.get('name', professor_obj.name)
        professor_obj.description = data.get('description', professor_obj.description)
        professor_obj.name_arabic = data.get('name_arabic', professor_obj.name_arabic)
        professor_obj.description_arabic = data.get('description_arabic', professor_obj.description_arabic)
        session.commit()
        return jsonify({"message": "professor updated successfully"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@chat_bot.route('/professor/<int:professor_id>', methods=['DELETE'])
def delete_professor(professor_id):
    session = get_uploaded_session()
    try:
        professor_obj = session.query(Professor).get(professor_id)
        if not professor_obj:
            return jsonify({"error": "professor not found"}), 404
        session.delete(professor_obj)
        session.commit()
        return jsonify({"message": "professor deleted successfully"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
#Question
@chat_bot.route('/question', methods=['GET'])
def get_question():
    try:
        session = get_uploaded_session()
        question_list = session.query(CourseQuestion).all()
        return jsonify([
            {
                "id": question.id,
                "question": question.question,
                "course_id": question.course_id,
                "question_arabic": question.question_arabic,
            }
            for question in question_list
        ])
    except Exception as e:
        print("Error in get_question:", e)
        return jsonify({'error': str(e)}), 500
@chat_bot.route('/question', methods=['POST'])
def create_question():
    session = get_uploaded_session()
    try:
        data = request.get_json()
        new_question = CourseQuestion(
            question=data['question'],
            course_id=data['course_id'],
            question_arabic=data['question_arabic'],
        )
        session.add(new_question)
        session.commit()
        return jsonify({"message": "question  created successfully", "id": new_question.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@chat_bot.route('/question/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    session = get_uploaded_session()
    try:
        question_obj = session.query(CourseQuestion).get(question_id)
        if not question_obj:
            return jsonify({"error": "question not found"}), 404
        data = request.get_json()
        question_obj.question = data.get('question',question_obj.question)
        question_obj.course_id = data.get('course_id', question_obj.course_id)
        question_obj.question_arabic = data.get('question_arabic', question_obj.question_arabic)
        session.commit()
        return jsonify({"message": "question updated successfully"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@chat_bot.route('/question/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    session = get_uploaded_session()
    try:
        question_obj = session.query(CourseQuestion).get(question_id)
        if not question_obj:
            return jsonify({"error": "question not found"}), 404
        session.delete(question_obj)
        session.commit()
        return jsonify({"message": "question deleted successfully"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
#json
@chat_bot.route("/list_json_files", methods=["GET"])
def list_json_files():
    try:
        print("BASE_DIR:", BASE_DIR)
        all_json_files = []
        for root, dirs, files in os.walk(BASE_DIR):
            for f in files:
                if f.endswith(".json"):
                    relative_path = os.path.relpath(os.path.join(root, f), BASE_DIR)
                    all_json_files.append(relative_path.replace("\\", "/"))  # للويندوز
        print("JSON Files:", all_json_files)  # طباعة الملفات
        return jsonify(all_json_files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chat_bot.route("/get_json/<path:filename>", methods=["GET"])
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

@chat_bot.route("/save_json/<filename>", methods=["POST"])
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

#Prerequisites
@chat_bot.route('/pre', methods=['GET'])
def get_pre():
    try:
        session = get_uploaded_session()
        pre_obj = session.query(course_prerequisites).all()
        return jsonify([
            {
                "course_id": pre.course_id,
                "prerequisite_id": pre.prerequisite_id,
            }
            for pre in pre_obj
        ])
    except Exception as e:
        print("Error in get_pre:", e)
        return jsonify({'error': str(e)}), 500
#course_professor
@chat_bot.route('/prof', methods=['GET'])
def get_prof():
    try:
        session = get_uploaded_session()
        prof_obj = session.query(course_professor).all()
        return jsonify([
            {
                "course_id": prof.course_id,
                "professor_id": prof.professor_id,
            }
            for prof in prof_obj
        ])
    except Exception as e:
        print("Error in get_prof:", e)
        return jsonify({'error': str(e)}), 500
#new table
@chat_bot.route('/get-tables/<db_name>', methods=['GET'])
def get_tables(db_name):
    db_file = f"{db_name}.db"  # مثال: university_information.db

    # اتأكد إن الملف موجود
    if not os.path.exists(db_file):
        return jsonify({"error": f"Database '{db_file}' does not exist."}), 404

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]

        conn.close()
        return jsonify(tables)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chat_bot.route('/create-table/<db_name>', methods=['POST'])
def create_table(db_name):
    if not request.is_json:
        return jsonify({"error": "Expected JSON format"}), 415

    data = request.get_json()
    table_name = data.get("name")

    if not table_name:
        return jsonify({"error": "Table name is required."}), 400

    if not table_name.replace("_", "").isalnum():
        return jsonify({"error": "Invalid table name."}), 400

    uploaded_db_path = f"{db_name}.db"
    if not os.path.exists(uploaded_db_path):
        return jsonify({"error": f"Database '{db_name}' does not exist."}), 404

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
        return jsonify({"message": f"Table '{table_name}' created successfully in database '{db_name}'."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@chat_bot.route('/delete-table/<db_name>', methods=['DELETE'])
def delete_table(db_name):
    if not request.is_json:
        return jsonify({"error": "Expected JSON format"}), 415

    data = request.get_json()
    table_name = data.get("name")

    if not table_name:
        return jsonify({"error": "Table name is required."}), 400

    if not os.path.exists(uploaded_db_path):
        return jsonify({"error": f"Database '{db_name}' does not exist."}), 404

    try:
        conn = sqlite3.connect(uploaded_db_path)
        cursor = conn.cursor()
        cursor.execute(f'DROP TABLE IF EXISTS "{table_name}"')
        conn.commit()
        conn.close()
        return jsonify({"message": f"Table '{table_name}' deleted successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#new table edit
def get_connection(db_name):
    conn = sqlite3.connect(f"./{db_name}.db")
    conn.row_factory = sqlite3.Row
    return conn, conn.cursor()
def close_connection(conn):
    conn.commit()
    conn.close()
@chat_bot.route("/get-table/<db_name>/<table_name>", methods=["GET"])
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

@chat_bot.route("/add-row/<db_name>/<table_name>", methods=["POST"])
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

@chat_bot.route("/update-row/<db_name>/<table_name>", methods=["POST"])
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

@chat_bot.route("/delete-row/<db_name>/<table_name>", methods=["POST"])
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

@chat_bot.route("/add-attribute/<db_name>/<table_name>", methods=["POST"])
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

if __name__ == '__main__':

    http_server = WSGIServer(
        ('0.0.0.0', 3001),
        chat_bot,
        keyfile=variables.key_loc,
        certfile=variables.cert_loc
    )
    try:
        print("Starting server...")
        http_server.serve_forever()
    except Exception as e:
        print(f"Error starting server... {e}")