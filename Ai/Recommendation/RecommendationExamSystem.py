import json
from Data.dataStorage import DataStorage
import variables

class Recommendation:
    def _init_(self, json_path=variables.MapDataLocationRE,
                 json_path2=variables.ResponseDataLocationRE):
        self.task_definitionsR = self.load_definitions(json_path)
        self.responses = self.load_responses(json_path2)
        self.storage = DataStorage()

    def load_definitions(self, json_path: str) -> dict:
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                print(f"[INFO] mapR file loaded successfully: {json_path}")
                return json.load(file)
        except FileNotFoundError:
            print(f"[ERROR] mapR file not found: {json_path}")
            return {}
        except json.JSONDecodeError:
            print(f"[ERROR] Invalid JSON format in: {json_path}")
            return {}

    def load_responses(self, json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                responses = json.load(file)
                print(f"[INFO] ResponseR file loaded successfully: {json_path}")

                if "exam_data" in responses:
                    return responses["exam_data"]
                else:
                    print("[ERROR] Key 'exam_data' not found in JSON!")
                    return []

        except FileNotFoundError:
            print(f"[ERROR] ResponseR file not found: {json_path}")
            return []
        except json.JSONDecodeError:
            print(f"[ERROR] Invalid JSON format in: {json_path}")
            return []

    def handle_exam_recommendation(self, user_input, user_id):
        prev_data = self.storage.get_prev_data(user_id)

        if not isinstance(prev_data, dict):
            print(f"[ERROR] Invalid prev_data format: {prev_data}")
            prev_data = {}
        print("[DEBUG] Asking for department first")

        if "department" not in prev_data or not prev_data["department"].strip():
            self.storage.save_data(user_id, "department", user_input.strip().lower())
            prev_data = self.storage.get_prev_data(user_id)

            if not prev_data.get("department") or prev_data["department"].strip() == "":
                return "what is your department?", ["cs", "cs & math", "cs & stat", "cs & phy"]

            return "What is your academic year?", ["Freshman", "Sophomore", "Junior", "Senior"]

        if "year" not in prev_data:
            self.storage.save_data(user_id, "year",  user_input.strip().lower())
            prev_data = self.storage.get_prev_data(user_id)
            return "What is your semester?", ["one", "two"]

        if "semester" not in prev_data:
            self.storage.save_data(user_id, "semester",  user_input.strip().lower())
            prev_data = self.storage.get_prev_data(user_id)
            if (prev_data["year"].strip() == "Sophomore" and
                    prev_data["semester"].strip() == "one"):
                return "What is the subject name?", ["algorithm", "computability", "oop","database"
                    ,"linear algebra","english"]
            elif (prev_data["year"].strip() == "Sophomore" and
                    prev_data["semester"].strip() == "two"):
                return "What is the subject name?", ["data structure", "network", "web programming"
                    ,"automata","graph","ordinary differential equation"]
            elif (prev_data["year"].strip() == "Junior" and
                    prev_data["semester"].strip() == "one"):
                return "What is the subject name?", ["java", "syntax", "complexity"
                    , "operating system", "abstract algebra", "multimedia","scientific thinking"]
            elif (prev_data["year"].strip() == "Junior" and
                  prev_data["semester"].strip() == "two"):
                return "What is the subject name?", ["scientific research ethics"
                    , "combinatorics", "compiler"
                    , "graphics", "android", "advanced data base","crybto"]
            elif (prev_data["year"].strip() == "senior" and
                  prev_data["semester"].strip() == "one"):
                return "What is the subject name?", ["skills", "artificial intelligence", "parallel"
                    , "project", "image processing", "cyber security","Computational geometry"]
            elif (prev_data["year"].strip() == "senior" and
                  prev_data["semester"].strip() == "two"):
                return "What is the subject name?", ["bioinformatics", "software engineering"
                    , "project", "advanced artificial intelligence", "data mining"]

        if "subject" not in prev_data:
            self.storage.save_data(user_id, "subject",  user_input.strip().lower())
            prev_data = self.storage.get_prev_data(user_id)
            if (prev_data["year"].strip() == "Sophomore" and
                    prev_data["semester"].strip() == "one"):
                    return "Who is the professor?", ["dr niveen", "dr dowlt","dr niveen , dr dowlt"
                        ,"dr ghada","dr wael","dr manar", "dr ahmed","dr manar,dr ahmed","dr abdelrahman"]
            elif (prev_data["year"].strip() == "Sophomore" and
                          prev_data["semester"].strip() == "two"):
                    return "Who is the professor?", ["dr wael", "dr ghada","dr wael , dr ghada"
                        , "dr hussein", "dr mohamed", "dr nashwa" ,"dr mohamed , dr nashwa","dr azaa"
                        ,"dr neveen","dr hany", "dr samir","dr hany & dr samir"]
            elif (prev_data["year"].strip() == "Junior" and
                  prev_data["semester"].strip() == "one"):
                return "Who is the professor?", ["dr nashwa",  "dr azza","dr neveen"
                    ,"dr mohamed","dr mohamed & dr neveen"
                    , "dr ahmed", "dr hussein", "dr abdelrahman"]
            elif (prev_data["year"].strip() == "Junior" and
                  prev_data["semester"].strip() == "two"):
                return "Who is the professor?", ["dr abdelrahman", "dr neveen", "dr wael"
                    , "dr hussein", "dr deiaa"]
            elif (prev_data["year"].strip() == "senior" and
                  prev_data["semester"].strip() == "one"):
                return "Who is the professor?", ["dr mohamed", "dr azza", "dr mohamed fakhry"
                    ,"dr hewayda","dr deiaa", "dr ghada"]
            elif (prev_data["year"].strip() == "senior" and
                  prev_data["semester"].strip() == "two"):
                return "Who is the professor?", ["dr mohamed hashim","dr mohamed fakhry"
                    ,"dr mohamed hashim ,dr mohamed fakhry", "dr hussein"
                    , "dr azza","dr hewayda","dr hewayda , dr azza", "dr dowlt"]

        exam_system_result = self.get_exam_system(prev_data, user_id)
        if isinstance(exam_system_result, str):
            return exam_system_result, []
        elif isinstance(exam_system_result, tuple) and len(exam_system_result) == 2:
            return exam_system_result
        else:
            return "Unexpected error occurred while retrieving exam system.", []

    def get_exam_system(self, prev_data, user_id):

        if not isinstance(prev_data, dict):
            return "Error: Invalid data format", []

        for exam in self.responses:
            if (prev_data["department"].lower() in [d.lower() for d in exam["department"]] and
                    prev_data["year"].lower() in [y.lower() for y in exam["level"]] and
                    prev_data["semester"].lower() in [s.lower() for s in exam["semester"]] and
                    prev_data["subject"].lower() in [sub.lower() for sub in exam["subject"]]):

                print(f"[INFO] Match found! Exam system: {exam['exam_format']}")
                self.storage.clear_data(user_id, keep_task=False)
                return f"The exam system for {prev_data['subject']} is: {exam['exam_format']}", []

            else:
                print(f"[WARNING] No match for: {prev_data}")

        return "No exam data available for this subject.", []