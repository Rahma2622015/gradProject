from flask import jsonify, request
from Modules.functions_json import jsonFunction
from Ai.RecivingFunction import receive
from Modules.server_instance import server_function


json_function=jsonFunction()

def messages():
    try:
        message = request.get_json()
        user_message = message.get('userMessage', '')
        client_id = message.get('id', '')

        client = server_function.get_client_by_id(client_id)


        if not client:
            return jsonify({"error": "Please start new session!"}), 404  # Not Found
        if not user_message:
            return jsonify({"error": "Message is required"}), 400  # Bad Request
        if not client_id:
            return jsonify({"error": "Client ID is required"}), 400  # Bad Request

        try:
            reply_text, reply_list, _ = receive(user_message, client.data, client_id)

            for c in server_function.client_list:
                if c.endSession():
                    server_function.client_list.remove(c)
                    json_function.remove_data(c.id)

            return jsonify({"reply": reply_text, "list": reply_list})

        except Exception as ex:
            return jsonify({"error": f"Error in receiving reply: {str(ex)}"})


    except Exception as e:
        return jsonify({"error":f"Error in send :{str(e)}"})