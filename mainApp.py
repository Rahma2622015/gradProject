import os
import variables
from flask import Flask
from flask_cors import CORS
from gevent.pywsgi import WSGIServer

from routes.session_routes import session_blueprint
from routes.message_routes import message_blueprint
from routes.course_routes import course_blueprint
from routes.upload_routes import upload_blueprint
from routes.answers_routes import answers_blueprint
from routes.question_routes import question_blueprint
from routes.json_routes import json_blueprint
from routes.prerequisite_routes import prerequisite_blueprint
from routes.professor_routes import professor_blueprint
from routes.course_professor_routes import course_professor_blueprint
from routes.new_table_routes import new_table_blueprint
from routes.table_routes import table_blueprint

chat_bot = Flask(__name__)
chat_bot.secret_key = os.urandom(24)
CORS(chat_bot)

chat_bot.register_blueprint(session_blueprint)
chat_bot.register_blueprint(message_blueprint)
chat_bot.register_blueprint(course_blueprint)
chat_bot.register_blueprint(upload_blueprint)
chat_bot.register_blueprint(answers_blueprint)
chat_bot.register_blueprint(professor_blueprint)
chat_bot.register_blueprint(question_blueprint)
chat_bot.register_blueprint(json_blueprint)
chat_bot.register_blueprint(prerequisite_blueprint)
chat_bot.register_blueprint(table_blueprint)
chat_bot.register_blueprint(course_professor_blueprint)
chat_bot.register_blueprint(new_table_blueprint)


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