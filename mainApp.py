import os
import json
import random
from Data.class_client import Client
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from Ai.RecivingFunction import receive
from gevent.pywsgi import WSGIServer
from OpenSSL import SSL

chat_bot = Flask(__name__)
data_file='session_data.json'
client_list=[]
chat_bot.secret_key = os.urandom(24)

CORS(chat_bot, resources={r"/messages": {"origins": "https://192.168.1.6:3000", "methods": ["POST", "GET"]}})
CORS(chat_bot, resources={r"/start-session": {"origins": "https://192.168.1.6:3000", "methods": ["POST"]}})
CORS(chat_bot, resources={r"/close-session": {"origins": "https://192.168.1.6:3000", "methods": ["POST"]}})


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
        client_id = session.get('client_id')

        if not client_id:
            return jsonify({"error": "No active session!"}), 400  # Bad Request

        client_to_remove = get_client_by_id(client_id)

        if client_to_remove:
            remove_data(client_id)
            client_list.remove(client_to_remove)
            return jsonify({"message": "Session closed", "client_id": client_id})
        else:
            return jsonify({"error": "Client ID not found!"}), 404  # Not Found
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
            reply = f"{receive(user_message, client.data)}"

            for c in client_list:
                if c.endSession():
                    client_list.remove(c)
                    remove_data(c.id)

            return jsonify({"reply": reply})

        except Exception as ex:
            return jsonify({"error": f"Error in receiving reply: {str(ex)}"}), 500  # Internal Server Error

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


if __name__ == '__main__':

    http_server = WSGIServer(
        ('0.0.0.0', 3001),
        chat_bot,
        keyfile='D:/Chatbot/private.key',
        certfile='D:/Chatbot/cert.crt'
    )
    try:
        print("Starting server...")
        http_server.serve_forever()
    except Exception as e:
        print(f"Error starting server... {e}")
