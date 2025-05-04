class DataStorage:
    def __init__(self):
        self.data = {}  # بيانات عامة
        self.session_data = {}  # بيانات الجلسة
        self.course_scores = {}  # درجات المواد

    # --- إدارة الجلسة ---
    def set_value(self, key, value, strict=True):
        if not strict or (key and value is not None):
            self.session_data[key] = value

    def get_value(self, key):
        return self.session_data.get(key)

    def clear_data(self, keep_task=False):
        if keep_task and "current_task" in self.session_data:
            self.session_data = {"current_task": self.session_data["current_task"]}
        else:
            self.session_data.clear()

    def get_prev_data(self):
        return self.session_data

    def set_current_task(self, task_name):
        self.set_value("current_task", task_name)

    def get_current_task(self):
        return self.get_value("current_task")

    def set_user_id(self, user_id):
        self.set_value("user_id", user_id)

    def get_user_id(self):
        return self.get_value("user_id")

    # --- إدارة الدرجات ---
    def save_course_score(self, course_name, score):
        self.course_scores[course_name] = score

    def get_course_score(self, course_name):
        return self.course_scores.get(course_name)

    def get_all_course_scores(self):
        return self.course_scores

    def get_top_courses(self, top_n=None):
        sorted_courses = sorted(self.course_scores.items(), key=lambda item: item[1], reverse=True)
        return sorted_courses[:top_n] if top_n else sorted_courses

    # --- إدارة البيانات العامة ---
    def add_data(self, name, value):
        if name not in self.data:
            self.data[name] = value
            return True
        return False

    def find_name(self, name):
        return name in self.data

    def find_value(self, value):
        return value in self.data.values()

    def fetch_name(self, value):
        for k, v in self.data.items():
            if v == value:
                return (k, v)
        return False

    def fetch_value(self, name):
        return self.data.get(name, False)

    def update_data(self, name, new_value):
        if self.find_name(name):
            self.data[name] = new_value
            return True
        return False

    def delete_data(self, name):
        return self.data.pop(name, None) is not None

    # --- أخرى ---
    def clear_all_data(self):
        self.data.clear()
        self.session_data.clear()
        self.course_scores.clear()

    def __str__(self):
        return f"Session: {self.session_data}, Scores: {self.course_scores}, Data: {self.data}"
