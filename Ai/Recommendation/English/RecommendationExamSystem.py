import json
from Data.dataStorage import DataStorage
import variables

class Recommendation:
    def __init__(self, json_path=variables.MapDataLocationEn,
                 json_path2=variables.ResponseDataLocationRE):
        self.task_definitionsR = self.load_definitions(json_path)
        self.responses = self.load_responses(json_path2)
        self.prev_data = {}

    def load_definitions(self, json_path: str) -> dict:
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                print(f"[INFO] mapR file loaded successfully: {json_path}")
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERROR] Unable to load mapR file: {e}")
            return {}

    def load_responses(self, json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                responses = json.load(file)
                print(f"[INFO] ResponseR file loaded successfully: {json_path}")
                return responses.get("exam_data", [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERROR] Unable to load ResponseR file: {e}")
            return []

    def handle_exam_recommendation(self, user_input):
        if not isinstance(self.prev_data, dict):
            print(f"[ERROR] Invalid prev_data format: {self.prev_data}")
            self.prev_data = {}
        print("[DEBUG] Asking for department first")

        if "department" not in self.prev_data or not self.prev_data["department"].strip():
            self.prev_data["department"] = user_input.strip().lower()

            if not self.prev_data.get("department") or self.prev_data["department"].strip() == "":
                return "what is your department?", ["cs", "cs & math", "cs & stat", "cs & phy"]

            return "What is your academic year?", ["freshman", "sophomore", "junior", "senior"]

        if "year" not in self.prev_data:
            self.prev_data["year"] = user_input.strip().lower()
            return "What is your semester?", ["one", "two"]

        if "semester" not in self.prev_data:
            self.prev_data["semester"] = user_input.strip().lower()
            return "What is the subject name?", self.get_subject_options()

        if "subject" not in self.prev_data:
            self.prev_data["subject"] = user_input.strip().lower()
            return "Who is the professor?", self.get_professor_options()

        return self.get_exam_system()

    def get_subject_options(self):
        subjects = {
            ("sophomore", "one"): ["algorithm", "computability", "oop", "database", "linear algebra", "english"],
            ("sophomore", "two"): ["data structure", "network", "web programming", "automata", "graph", "ordinary differential equation"],
            ("junior", "one"): ["java", "syntax", "complexity", "operating system", "abstract algebra", "multimedia", "scientific thinking"],
            ("junior", "two"): ["scientific research ethics", "combinatorics", "compiler", "graphics", "android", "advanced data base", "crypto"],
            ("senior", "one"): ["skills", "artificial intelligence", "parallel", "project", "image processing", "cyber security", "Computational geometry"],
            ("senior", "two"): ["bioinformatics", "software engineering", "project", "advanced artificial intelligence", "data mining"]
        }
        return subjects.get((self.prev_data.get("year"), self.prev_data.get("semester")), [])

    def get_professor_options(self):
        professors = {
            ("sophomore", "one"): ["dr niveen", "dr dowlt", "dr ghada", "dr wael", "dr manar", "dr ahmed", "dr niveen , dr dowlt", "dr manar , dr ahmed"],
            ("sophomore", "two"): ["dr wael", "dr ghada", "dr hussein", "dr mohamed", "dr nashwa", "dr azaa", "dr wael , dr ghada", "dr mohamed , dr nashwa", "dr hany & dr samir"],
            ("junior", "one"): ["dr nashwa", "dr azza", "dr neveen", "dr mohamed", "dr ahmed", "dr hussein", "dr mohamed & dr neveen"],
            ("junior", "two"): ["dr abdelrahman", "dr neveen", "dr wael", "dr hussein", "dr deiaa"],
            ("senior", "one"): ["dr mohamed", "dr azza", "dr mohamed fakhry", "dr hewayda", "dr deiaa", "dr ghada"],
            ("senior", "two"): ["dr mohamed hashim", "dr mohamed fakhry", "dr hussein", "dr azza", "dr hewayda", "dr dowlt", "dr mohamed hashim , dr mohamed fakhry", "dr hewayda , dr azza"]
        }
        return professors.get((self.prev_data.get("year"), self.prev_data.get("semester")), [])

    def get_exam_system(self):
        for exam in self.responses:
            if (self.prev_data["department"].lower() in [d.lower() for d in exam["department"]] and
                self.prev_data["year"].lower() in [y.lower() for y in exam["level"]] and
                self.prev_data["semester"].lower() in [s.lower() for s in exam["semester"]] and
                self.prev_data["subject"].lower() in [sub.lower() for sub in exam["subject"]]):
                print(f"[INFO] Match found! Exam system: {exam['exam_format']}")
                self.prev_data.clear()
                return f"The exam system for {exam['subject']} is: {exam['exam_format']}", []

        print(f"[WARNING] No match for: {self.prev_data}")
        return "No exam data available for this subject.", []
