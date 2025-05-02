import json
import variables

class ArRecommendation:
    def __init__(self, json_path=variables.MapDataLocationAr,
                 json_path2=variables.ArResponseDataLocationRE):
        self.task_definitionsR = self.load_definitions(json_path)
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

    def load_responses(self, json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                responses = json.load(file)
                print(f"[INFO] Arabic Response file loaded successfully: {json_path}")
                return responses.get("exam_data", [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERROR] Unable to load Arabic Response file: {e}")
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
            return "ما اسم الدكتور؟", self.get_professor_options()
        self.prev_data["professor"]=user_input.strip().lower()

        if ("department" in self.prev_data and "year" in self.prev_data and
                "semester" in self.prev_data and "subject" in self.prev_data and
                "professor" in self.prev_data):
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
                , "اوتوماتا", "جراف", "رياضه"],
            ("تالته", "اول"): ["جافا", "سينتاكس", "تعقد", "نظم التشغيل"
                , "رياضه", "مالتى ميديا", "تفكير العلمى"],
            ("تالته", "تانى"): ["اخلاقيات البحث العلمى", "كومبيناتركس", "كومبلير"
                , "جرافكس", "اندرويد", "داتابيز متقدمه", "كريبتو"],
            ("رابعه", "اول"): ["مهارات", "ذكاء اصطناعى", "بارليل", "مشروع"
                , "ايمدج", "سايبر", "جيمتورى"],
            ("رابعه", "تانى"): ["بايو", "سوفت وير", "مشروع"
                , "ذكاء اصطناعى متقدمة", "داتا ماينيج"]
        }
        return subjects.get((self.prev_data.get("year"), self.prev_data.get("semester")), [])


    def get_professor_options(self):
        professors = {
            ("اولى", "اول"): ["دكتور عبدالرحمن", "دكتور عصام", "دكتور هبه", "دكتور سيد", "دكتور هبه , دكتور سيد"
                , "دكتور محمد عماد", "دكتور ايمن", "دكتور محمد عماد , دكتور ايمن",
                                  "دكتور ايات"],
            ("اولى", "تانى"): ["دكتور هانى", "دكتور منار", "دكتور احمد جابر", "دكتور منار , دكتور احمد جابر"
                , "دكتور نشوى", "دكتور محمد فخرى", "دكتور ضياء", "دكتور محمد فخرى , دكتور ضياء",
                                  "دكتور نجلاء", "دكتور عبدالرحمن"],

            ("تانية", "اول"): ["دكتور نيفين", "دكتور دولت", "دكتور غادة",
                                   "دكتور وائل", "دكتور منار"
                    , "دكتور احمد", "دكتور نيفين و دكتور دولت", "دكتور منار و دكتور احمد"],
            ("تانية", "تانى"): ["دكتور وائل", "دكتور غادة", "دكتور حسين", "دكتور محمد"
                    , "دكتور نشوى", "دكتور عزة", "دكتور وائل و دكتور غادة"
                    , "دكتور محمد و دكتور نشوى", "دكتور هانى و دكتور سمير"],
            ("تالته", "اول"): ["دكتور نشوى", "دكتور عزة", "دكتور نيفين", "دكتور محمد"
                    , "دكتور احمد", "دكتور حسين", "دكتور نيفين و دكتور محمد"],
            ("تالته", "تانى"): ["دكتور عبدالرحمن", "دكتور نيفين", "دكتور وائل",
                                    "دكتور حسين", "دكتور ضياء"],
            ("رابعه", "اول"): ["دكتور فخرى", "دكتور عزة", "دكتور هوايدا"
                    , "دكتور ضياء", "دكتور غادة"],
            ("رابعه", "تانى"): ["دكتور هاشم ", "دكتور فخرى"
                    , "دكتور حسين", "دكتور عزة", "دكتور هوايدا", "دكتور دولت"
                    , "دكتور فخرى و دكتور هاشم", "دكتور هوايدا و دكتور عزة"]
        }
        return professors.get((self.prev_data.get("year"), self.prev_data.get("semester")), [])

    def get_exam_system(self):
        for exam in self.responses:
            if (self.prev_data["department"].lower() in [d.lower() for d in exam["department"]] and
                    self.prev_data["year"].lower() in [y.lower() for y in exam["level"]] and
                    self.prev_data["semester"].lower() in [s.lower() for s in exam["semester"]] and
                    self.prev_data["subject"].lower() in [sub.lower() for sub in exam["subject"]] and
                    self.prev_data["professor"].lower() in [pro.lower() for pro in exam["instructor"]]):

                print(f"[INFO] Match found! Exam system: {exam['exam_format']}")
                exam_format = exam['exam_format']
                parts = []

                if "منتصف الترم" in exam_format:
                    parts.append(f"امتحان منتصف الترم: {', '.join(exam_format['منتصف الترم'])}")
                if "النهائى" in exam_format:
                    parts.append(f"الامتحان النهائي: {', '.join(exam_format['النهائى'])}")
                if "مشروع" in exam_format:
                    parts.append(f"مشروع المادة: {', '.join(exam_format['مشروع'])}")

                exam_system_str = " و ".join(parts)
                self.prev_data.clear()

                subject_name = ', '.join(exam['subject']) if isinstance(exam['subject'], list) else exam['subject']
                return f"نظام الامتحانات لمادة {subject_name} هو: {exam_system_str}", []

        print(f"[WARNING] No match for: {self.prev_data}")
        self.prev_data.clear()
        return "لا توجد بيانات متاحة لنظام الامتحان لهذه المادة.", []
