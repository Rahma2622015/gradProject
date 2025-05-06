import os
import json

class jsonFunction:

    def load_data(self,data_file):
        if not os.path.exists(data_file):
            return {}
        try:
            with open(data_file, 'r') as file:
                data = json.load(file)
                if not isinstance(data, dict):
                    raise ValueError("Modules is not in the correct format!")
                return data
        except (json.JSONDecodeError, ValueError) as e:
            return {}

    def save_data(self,data,data_file):
        with open(data_file, 'w') as file:
            json.dump(data, file)

    def remove_data(self,client_id,data_file):
        try:
            client_data = self.load_data(data_file)
            if str(client_id) in client_data:
                del client_data[str(client_id)]
                self.save_data(client_data,data_file)
        except Exception as e:
            print(f"Error removing data item: {e}")