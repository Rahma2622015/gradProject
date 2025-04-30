class DataStorage:
    def __init__(self):
        self.data = {}  # لتخزين البيانات العامة
        self.session_data = {}  # لتخزين البيانات الخاصة بكل جلسة
        self.course_scores = {}  # لتخزين درجات المواد

    def get_value(self, key):
        """ استرجاع القيمة بناءً على المفتاح (بدون استخدام user_id) """
        return self.session_data.get(key, None)

    def set_value(self, key, value):
        """ تعيين قيمة لمفتاح معين (بدون استخدام user_id) """
        self.session_data[key] = value

    def save_course_score(self, course_name, score):
        """ حفظ درجة مادة معينة """
        self.course_scores[course_name] = score

    def get_course_score(self, course_name):
        """ استرجاع درجة مادة معينة """
        return self.course_scores.get(course_name, None)

    def get_all_course_scores(self):
        """ استرجاع جميع درجات المواد """
        return self.course_scores

    def get_top_courses(self, top_n=None):
        """ استرجاع أفضل المواد بناءً على الدرجات """
        sorted_courses = sorted(self.course_scores.items(), key=lambda item: item[1], reverse=True)
        if top_n is not None:
            sorted_courses = sorted_courses[:top_n]
        return sorted_courses

    def addData(self, name, value):
        """ إضافة بيانات جديدة """
        if name not in self.data:
            self.data[name] = value
            return True
        return False

    def findName(self, name):
        """ البحث عن اسم معين في البيانات """
        return name in self.data

    def findValue(self, value):
        """ البحث عن قيمة معينة في البيانات """
        return value in self.data.values()

    def fetchName(self, value):
        """ استرجاع الاسم المرتبط بقيمة معينة """
        for item in self.data.items():
            if item[1] == value:
                return item
        else:
            return False

    def fetchValue(self, name):
        """ استرجاع القيمة المرتبطة باسم معين """
        return self.data.get(name, False)

    def updateData(self, name, newValue):
        """ تحديث البيانات لاسم معين """
        if self.findName(name):
            self.data[name] = newValue
            return True
        return False

    def deleteData(self, name):
        """ حذف بيانات لاسم معين """
        if self.findName(name):
            self.data.pop(name)
            return True
        return False

    def get_prev_data(self):
        """ استرجاع البيانات السابقة للجلسة الحالية """
        print(f"[DEBUG] get_prev_data: {self.session_data}")
        return self.session_data

    def save_data(self, key, value):
        """ حفظ البيانات لجلسة معينة مع التحقق من القيم الفارغة """
        if key and value:
            self.session_data[key] = value
        else:
            print("[WARNING] Invalid data. Key or value is None.")

    def clear_data(self, keep_task=False):
        """ مسح بيانات الجلسة (مع إمكانية إبقاء بعض البيانات مثل task) """
        if keep_task:
            current_task = self.session_data.get("current_task")
            if current_task:
                self.session_data = {"current_task": current_task}
            else:
                self.session_data = {}
        else:
            self.session_data = {}

    def clear_all_data(self):
        """ مسح جميع البيانات المخزنة (البيانات العامة، الجلسة، درجات المواد) """
        self.data = {}
        self.session_data = {}
        self.course_scores = {}

    def set_current_task(self, task_name):
        """ تعيين المهمة الحالية """
        self.session_data["current_task"] = task_name

    def get_current_task(self):
        """ استرجاع المهمة الحالية """
        return self.session_data.get("current_task", None)

    def set_user_id(self, user_id):
        """ تعيين معرف المستخدم في الجلسة """
        self.session_data["user_id"] = user_id

    def get_user_id(self):
        """ استرجاع معرف المستخدم """
        return self.session_data.get("user_id", None)

    def log_update(self, action, key, value):
        """ تسجيل أي عملية تحديث تحدث """
        print(f"[LOG] {action} - Key: {key}, Value: {value}")

    def __str__(self):
        """ طباعة تفاصيل البيانات المخزنة """
        return f"Session Data: {self.session_data}, Course Scores: {self.course_scores}, General Data: {self.data}"

