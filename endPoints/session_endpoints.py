from flask import request, jsonify, session
from Modules.class_client import Client
from Modules.functions_json import jsonFunction
from Modules.server_instance import server_function


json_function=jsonFunction()

expired_clients = []

def start_session():
    try:
        client = Client()
        client_id = server_function.generateClientId()
        client.setClientId(client_id)
        client_data = json_function.load_data()

        client_data[str(client_id)] = {
            'id': client_id,
            'session_started': True
        }
        json_function.save_data(client_data)

        session['client_id'] = client_id

        server_function.client_list.append(client)



        for c in server_function.client_list:
            if c.endSession():
                expired_clients.append(c)

        for c in expired_clients:
            server_function.client_list.remove(c)
            json_function.remove_data(c.id)

        if client.startSession(client_id):
            return jsonify({"message": "Session started", "client_id": client_id})
        else:
            return jsonify({"error": "Failed to start session"}), 500

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

def close_session():
    try:
        data = request.get_json()
        client_id = data.get('client_id')

        if not client_id:
            return jsonify({"error": "Client ID is missing!"}), 400

        client_to_remove = server_function.get_client_by_id(client_id)

        if client_to_remove:
            json_function.remove_data(client_id)
            server_function.client_list.remove(client_to_remove)
            return jsonify({"message": "Session closed", "client_id": client_id})
        else:
            return jsonify({"error": "Client ID not found!"}), 404

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


