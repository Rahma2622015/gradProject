import json
import variables

class ArRecommendation:
    def __init__(self, json_path=variables.ArResponseDataDocLocationRE,
                 json_path2=variables.ArResponseDataLocationRE):
        self.doct=self.load_responsesDoc(json_path)
        self.responses = self.load_responses(json_path2)
        self.prev_data = {}

    def load_responsesDoc(self, json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                responses = json.load(file)
                print(f"[INFO] ResponseR doc file loaded successfully: {json_path}")
                return responses.get("exam_data", [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERROR] Unable to load ResponseR doc file: {e}")
            return []

    def load_responses(self, json_path2):
        try:
            with open(json_path2, "r", encoding="utf-8") as file:
                responses = json.load(file)
                print(f"[INFO] Arabic Response doc file loaded successfully: {json_path2}")
                return responses.get("exam_data", [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERROR] Unable to load Arabic Response doc file: {e}")
            return []

    def handle_exam_recommendation(self, user_input):
        if not isinstance(self.prev_data, dict):
            print(f"[ERROR] Invalid prev_data format: {self.prev_data}")
            self.prev_data = {}

        if "department" not in self.prev_data or not self.prev_data["department"].strip():
            self.prev_data["department"] = user_input.strip().lower()

            if not self.prev_data.get("department") or self.prev_data["department"].strip() == "":
                return "ما هو قسمك ؟", ["حاسب", "حاسب & رياضة", "حاسب & احصا", "حاسب & فيزيا"]

            return "ما هى السنة الدراسية", ["اولى", "تانية", "تالته", "رابعه"]

        if "year" not in self.prev_data:
            self.prev_data["year"] = user_input.strip().lower()
            return "ما هو الترم الذى تريد السؤال فيه؟", ["اول", "تانى"]

        if "semester" not in self.prev_data:
            self.prev_data["semester"] = user_input.strip().lower()
            return "ما اسم المادة؟", self.get_subject_options()

        if "subject" not in self.prev_data:
            self.prev_data["subject"] = user_input.strip().lower()
            return "ما اسم الدكتور؟", self.get_professor_options()

        self.prev_data["instructor"] = user_input.strip().lower()

        if ("department" in self.prev_data and "year" in self.prev_data and
                "semester" in self.prev_data and "subject" in self.prev_data and
                "instructor" in self.prev_data):
            print(self.prev_data)
            return self.get_exam_system()
        else:
            return "sorry the answer not matched with my data ", []

    def get_subject_options(self):
        subjects = {
            ("اولى","اول"):[ "امن و سلامة","حقوق الانسان", "تفاضل & تكامل","فيزياء" , "كيمياء"
                             ,"احصاء" ,],
            ("اولى","تانى"):[ "تفاضل & تكامل 2" ,"مفاهيم اساسية فى الرياضيات","مقدمة فى الحاسب الالى"
                             "برمجة حاسب", "تصميم منطق","انجليزى"],
            ("تانية", "اول"): ["الجوريزم", "كومبيتبلتى", "برمجة2", "داتابيز"
                , "رياضة", "انجليزى"],
            ("تانية", "تانى"): ["تركيب البيانات", "شبكات", "ويب"
                , "اوتوماتا", "جراف", "رياضة"],
            ("تالته", "اول"): ["جافا", "سينتاكس", "تعقد", "نظم التشغيل"
                , "رياضة", "مالتى ميديا", "تفكير العلمى"],
            ("تالته", "تانى"): ["اخلاقيات البحث العلمى", "كومبيناتركس", "كومبلير"
                , "جرافكس", "اندرويد", "داتابيز متقدمه", "كريبتو"],
            ("رابعه", "اول"): ["مهارات", "ذكاء اصطناعى", "بارليل", "مشروع"
                , "ايمدج", "سايبر", "جيمتورى"],
            ("رابعه", "تانى"): ["بايو", "سوفت وير", "مشروع"
                , "ذكاء اصطناعى متقدمة", "داتا ماينيج"]
        }
        return subjects.get((self.prev_data.get("year"), self.prev_data.get("semester")), [])

    def get_professor_options(self):
        category_subjects_map = {
            "حاسب": ["برمجة2", "تركيب البيانات", "ويب", "شبكات", "نظم التشغيل", "جافا", "اندرويد",
                     "كريبتو", "كومبلير", "جرافكس", "مالتى ميديا", "داتابيز", "داتابيز متقدمه",
                     "ذكاء اصطناعى", "ذكاء اصطناعى متقدمة", "مشروع", "سوفت وير" ,"بايو",
                     "برمجة حاسب","تصميم منطق" ,"اوتوماتا" ,"كومبيتبلتى" , "الجوريزم"
                     , "سينتاكس","كومبيناتركس","تعقد" , "ايمدج", "سايبر"
                    ,"بارليل", "جيمتورى","داتا ماينيج"],

            "رياضة": ["رياضة", "تفاضل & تكامل", "جيمتورى","احصاء" ,"تفاضل & تكامل 2"
                      ,"مفاهيم اساسية فى الرياضيات"  ],

            "فيزياء": [ "فيزياء"],

            "كيمياء": ["كيمياء"],

            "متطلب": ["اخلاقيات البحث العلمى", "مهارات", "تفكير العلمى"
                ,"امن و سلامة","حقوق الانسان","انجليزى"]
        }
        professor_by_category = {
            "حاسب":["دكتور نشوى" ,"دكتور محمد فخرى" ,"دكتور نيفين" ,"دكتور دولت", "دكتور غادة"
                   ,"دكتور ضياء" ,"دكتور محمد هاشم" ,"دكتور عزة","دكتور حسين" ,"دكتور هوايدا"],
            "رياضة": ["دكتور ايات" ,"دكتور هانى" , "دكتور منار", "دكتور احمد جابر"
                       , "دكتور سمير","دكتور احمد السنباطى","دكتور غادة" ,"دكتور عصام"],
            "فيزياء": ["دكتور هبه","دكتور سيد"],
            "كيمياء": ["دكتور ايمن ايوب" ,"دكتور محمد عماد"],
            "متطلب": ["دكتور عبدالرحمن","دكتور محمد"]
        }

        subject = self.prev_data.get("subject", "").strip()
        category = next((cat for cat, subjects in category_subjects_map.items() if subject in subjects), "متطلب")

        return professor_by_category.get(category, [])

    def get_exam_system(self):
        exam_system_response = ""
        exam_format_message = ""

        def join_items(items):
            if not items:
                return ""
            if len(items) == 1:
                return items[0]
            return ', '.join(items[:-1]) + ' and ' + items[-1]

        if not exam_system_response:
            for doctor in self.doct:
                if self.prev_data["instructor"].lower() in [d.lower() for d in doctor['instructo']]:
                    professor_name = ', '.join(doctor['instructo']) if isinstance(doctor['instructo'], list) else \
                    doctor['instructo']
                    exam_sys = doctor["exam_system"]
                    exam_system_text = join_items(exam_sys)
                    exam_system_response = f"نظام الامتحان مع الدكتور {professor_name}: {exam_system_text}"
                    break

        if not exam_format_message:
            for exam in self.responses:
                if (self.prev_data["department"].lower() in [di.lower() for di in exam["department"]] and
                        self.prev_data["year"].lower() in [y.lower() for y in exam["level"]] and
                        self.prev_data["semester"].lower() in [s.lower() for s in exam["semester"]] and
                        self.prev_data["subject"].lower() in [sub.lower() for sub in exam["subject"]]):
                    exam_format = exam['topics']
                    subject_name = ', '.join(exam['subject']) if isinstance(exam['subject'], list) else exam['subject']
                    exam_format_text = join_items(exam_format)
                    exam_format_message = f"شكل امتحان مادة {subject_name}: {exam_format_text}"
                    break

        if not exam_format_message:
            exam_format_message = "لا يوجد معلومات عن شكل الامتحان لهذه المادة."
        if not exam_system_response:
            exam_system_response = "لا يوجد معلومات عن نظام الامتحان مع الدكتور."

        self.prev_data.clear()
        return f"{exam_format_message}\n{exam_system_response}", []
