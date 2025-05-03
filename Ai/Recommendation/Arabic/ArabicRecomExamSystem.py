import json
import variables

class ArRecommendation:
    def __init__(self, json_path=variables.ArResponseDataDocLocationRE,
                 json_path2=variables.ArResponseDataLocationRE):
        self.doct=self.load_definitions(json_path)
        self.responses = self.load_responses(json_path2)
        self.prev_data = {}

    def load_definitions(self, json_path: str) -> dict:
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: File {json_path} not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Failed to parse JSON from {json_path}.")
            return {}

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
            print(f"[خطأ] تنسيق بيانات غير صالح: {self.prev_data}")

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
            return "ما اسم الدكتور؟",["دكتور عبدالرحمن", "دكتور عصام", "دكتور هبه", "دكتور سيد"
                , "دكتور محمد عماد", "دكتور ايمن ايوب","دكتور هانى", "دكتور منار", "دكتور احمد جابر"
                , "دكتور نشوى", "دكتور محمد فخرى", "دكتور ضياء","دكتور ايات"
                ,"دكتور نيفين", "دكتور دولت", "دكتور غادة"
                , "دكتور عزة" , "دكتور هانى","دكتور سمير", "دكتور احمد السنباطى", "دكتور حسين"
                , "دكتور هوايدا" ,"دكتور محمد هاشم"
            ]
        self.prev_data["instructor"]=user_input.strip().lower()

        if ("department" in self.prev_data and "year" in self.prev_data and
                "semester" in self.prev_data and "subject" in self.prev_data and
                "instructor" in self.prev_data):
            return self.get_exam_system()
        else:
            return "عذرًا، لم أتمكن من فهم البيانات بالكامل.", []


    def get_subject_options(self):
        subjects = {
            ("اولى", "اول"): ["امن و سلامة", "حقوق الانسان", "تفاضل & تكامل", "فيزياء", "كيمياء",
                                  "احصاء"],
            ("اولى", "تانى"): ["تفاضل & تكامل 2", "مفاهيم اساسية فى الرياضيات", "مقدمة فى الحاسب الالى", "برمجة حاسب",
                                  "تصميم منطق", "انجليزى"],
            ("تانية", "اول"): ["الجوريزم", "كومبيتبلتى", "برمجة2", "داتابيز"
                , "رياضة", "انجليزى"],
            ("تانية", "تانى"): ["تركيب البيانات", "شبكات", "ويب"
                , "اوتوماتا", "جراف", "رياضة"],
            ("تالته", "اول"): ["جافا", "سينتاكس", "تعقد", "نظم التشغيل"
                , "رياضه", "مالتى ميديا", "تفكير العلمى"],
            ("تالته", "تانى"): ["اخلاقيات البحث العلمى", "كومبيناتركس", "كومبلير"
                , "جرافكس", "اندرويد", "داتابيز متقدمه", "كريبتو"],
            ("رابعه", "اول"): ["مهارات العمل", "ذكاء اصطناعى", "بارليل", "مشروع"
                , "ايمدج", "سايبر", "جيمتورى"],
            ("رابعه", "تانى"): ["بايو", "سوفت وير"
                , "ذكاء اصطناعى متقدمة", "داتا ماينيج"]
        }
        return subjects.get((self.prev_data.get("year"), self.prev_data.get("semester")), [])

    def get_exam_system(self):
        exam_system_response = ""
        exam_format_message = ""

        if not exam_system_response:
            for doctor in self.doct:
                if self.prev_data["instructor"].lower() in [d.lower() for d in doctor["instructo"]]:
                    professor_name = ', '.join(doctor['instructo']) if isinstance(doctor['instructo'], list) else \
                    doctor['instructo']
                    exam_sys = doctor["exam_system"]
                    exam_system_text = ', '.join(exam_sys)
                    exam_system_response = f"نظام الامتحان ل{professor_name}: \n{exam_system_text}"
                    break
        if not exam_format_message:
            for exam in self.responses:
                if (self.prev_data["department"].lower() in [di.lower() for di in exam["department"]] and
                        self.prev_data["year"].lower() in [y.lower() for y in exam["level"]] and
                        self.prev_data["semester"].lower() in [s.lower() for s in exam["semester"]] and
                        self.prev_data["subject"].lower() in [sub.lower() for sub in exam["subject"]]):
                    exam_format = exam['topics']
                    subject_name = ', '.join(exam['subject']) if isinstance(exam['subject'], list) else exam['subject']

                    exam_format_text = ', '.join(exam_format)
                    exam_format_message = f"شكل الامتحان لمادة  {subject_name}:\n{exam_format_text}"
                    break

        if not exam_format_message:
            exam_format_message = "لا يوجد داتا متاحه لهذه المادة."
        if not exam_system_response:
            exam_system_response = "لا يوجد دكتور متاح نظامه."

        if exam_system_response and exam_format_message:
            return f"{exam_format_message}\n\n, {exam_system_response}", []
        self.prev_data.clear()
        return "لا يوجد نظام امتحانات متاح لهذه المعلومات", []
