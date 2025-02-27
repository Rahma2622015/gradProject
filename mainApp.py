#cd "D:\Chatbot\front_end"
#netstat -ano | findstr :3000
#taskkill /PID    /F
import random
import sys
import os
from gevent.pywsgi import WSGIServer
from Data.class_client import Client
from flask import Flask, request, jsonify
from flask_cors import CORS
from Ai.RecivingFunction import receive
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

chat_bot = Flask(__name__)

#context = SSL.Context(SSL.TLSv1_2_METHOD)
#context.use_certificate_file('SSL/server.cert')
#context.use_privatekey_file('SSL/server.key')

CORS(chat_bot, resources={r"/messages": {"origins": "https://192.168.1.6:3000", "methods": ["POST", "GET"]}})
CORS(chat_bot, resources={r"/start-session": {"origins": "https://192.168.1.6:3000", "methods": ["POST"]}})
CORS(chat_bot, resources={r"/close-session": {"origins": "https://192.168.1.6:3000", "methods": ["POST"]}})


client_list: list[Client] = []

def generateClientId():
    new_id = random.randint(1, 999999)

    while any(client.getClientId() == new_id for client in client_list):
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
        client_list.append(client)

        if client.startSession(client_id):
            return jsonify({"message": "Session started", "client_id": client_id})
        else:
            return jsonify({"error": "Failed to start session"}), 500

    except Exception as e:
        print(e)
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

@chat_bot.route('/close-session', methods=['POST'])
def close_session():
    try:
        c = request.get_json()
        client_id = c.get("client_id")

        if not client_id:
            return jsonify({"error": "Client ID is required"}), 400  # Bad Request

        client_to_remove = get_client_by_id(client_id)
        if client_to_remove:
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

        if client is None:
            return jsonify({"error": "Please start new session!"}), 404  # Not Found

        if client.endSession():
            client_list.remove(client)
            return jsonify({"message": "The time is up!"})

        #client.data.addData(client_id, user_message)

        if not user_message:
            return jsonify({"error": "Message is required"}), 400  # Bad Request

        if not client_id:
            return jsonify({"error": "Client ID is required"}), 400  # Bad Request
        try:
            reply = f"{receive(user_message, client.data)}"
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
        print(f"Error starting the server:{str(e)}")
