import json
from Data.dataStorage import DataStorage
import variables


class ArRecommendation:
    def __init__(self, json_path=variables.MapDataLocationAr,
                 json_path2=variables.ArResponseDataLocationRE):
        self.task_definitionsR = self.load_definitions(json_path)
        self.responses = self.load_responses(json_path2)
        self.storage = DataStorage()

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
        prev_data = self.storage.get_prev_data()

        if not isinstance(prev_data, dict):
            print(f"[ERROR] Invalid prev_data format: {prev_data}")
            prev_data = {}

        print("[DEBUG] Asking for department first")

        if "department" not in prev_data or not prev_data["department"].strip():
            self.storage.save_data("department", user_input.strip().lower())
            prev_data = self.storage.get_prev_data()

            if not prev_data.get("department") or prev_data["department"].strip() == "":
                return "ما هو قسمك ؟", ["حاسب", "حاسب & رياضة", "حاسب & احصا", "حاسب & فيزيا"]

            return "ما هى السنة الدراسية", ["اولى", "تانية", "تالته", "رابعه"]

        if "year" not in prev_data:
            self.storage.save_data("year", user_input.strip().lower())
            prev_data = self.storage.get_prev_data()
            return "ما هو الترم الذى تريد السؤال فيه؟", ["اول", "تانى"]

        if "semester" not in prev_data:
            self.storage.save_data("semester", user_input.strip().lower())
            return "ما اسم المادة؟", self.get_subject_options(prev_data)

        if "subject" not in prev_data:
            self.storage.save_data("subject", user_input.strip().lower())
            return "ما اسم الدكتور؟", self.get_professor_options(prev_data)

        return self.get_exam_system(prev_data)

    def get_subject_options(self, prev_data):
        subjects = {
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
        return subjects.get((prev_data.get("year"), prev_data.get("semester")), [])

    def get_professor_options(self, prev_data):
        professors = {
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
        return professors.get((prev_data.get("year"), prev_data.get("semester")), [])

    def get_exam_system(self, prev_data):
        for exam in self.responses:
            if (prev_data["department"].lower() in [d.lower() for d in exam["department"]] and
                    prev_data["year"].lower() in [y.lower() for y in exam["level"]] and
                    prev_data["semester"].lower() in [s.lower() for s in exam["semester"]] and
                    prev_data["subject"].lower() in [sub.lower() for sub in exam["subject"]]):
                print(f"[INFO] Match found! Exam system: {exam['exam_format']}")
                self.storage.clear_data(keep_task=False)
                return f"نظام الامتحان ل{prev_data['subject']} is: {exam['exam_format']}", []

        print(f"[WARNING] No match for: {prev_data}")
        return "لا يوجد نظام امتحانات متاح لهذه المعلومات", []
