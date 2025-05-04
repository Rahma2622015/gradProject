import random
from Modules.functions_json import jsonFunction

json_function=jsonFunction()

class serverFunction:

    def __init__(self):
        self.client_list=[]

    def generateClientId(self):
        new_id = random.randint(1, 999999)
        client_data = json_function.load_data()
        while str(new_id) in client_data:
            new_id = random.randint(1, 999999)
        return new_id

    def get_client_by_id(self,id):
        id = int(id)
        for c in self.client_list:
            if c.id == id:
                return c
        return None

