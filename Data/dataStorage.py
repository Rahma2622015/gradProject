class DataStorage:

    def __init__(self):
        self.data = {}
        self.session_data = {}

    def addData(self, name, value):
        if name not in self.data:
            self.data[name] = value
            return True
        return False

    def findName(self, name):
        return name in self.data

    def findValue(self,value):
        return value in self.data.values()

    def fetchName(self,value):
        for item in self.data.items():
            if item[1] == value:
                return item
        else :
            return False

    def fetchValue(self,name):
        for key,value in self.data.items():
            if name == key:
                return value
        return False

    def updateData(self,name,newValue):
        if self.findName(name):
            self.data[name] = newValue
            return True
        return False

    def deleteData(self,name):
        if self.findName(name):
            self.data.pop(name)
            return True
        return False

    def get_prev_data(self, user_id):
        data = self.session_data.get(user_id, {})
        return data

    def save_data(self, user_id, key, value):
        if not user_id or not key:
            return

        if user_id not in self.session_data:
            self.session_data[user_id] = {}

        self.session_data[user_id][key] = value

    def clear_data(self, user_id, keep_task=False):
        if user_id in self.session_data:
            if keep_task:
                current_task = self.session_data[user_id].get("current_task")
                if current_task:
                    self.session_data[user_id] = {"current_task": current_task}
                else:
                    del self.session_data[user_id]
            else:
                del self.session_data[user_id]

    def set_current_task(self, user_id, task_name):
        if user_id not in self.session_data:
            self.session_data[user_id] = {}

        self.session_data[user_id]["current_task"] = task_name

    def get_current_task(self, user_id):
        task = self.session_data.get(user_id, {}).get("current_task", None)
        return task

    def __str__(self):
        return str(self.data)
