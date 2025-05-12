import json
import variables

class Recommendation:
    def __init__(self,json_path=variables.ResponseDataLocationRE,json_path2=variables.ResponseDataDocLocation):
        self.responses = self.load_responses(json_path)
        self.doctors=self.load_responsesDoc(json_path2)
        self.prev_data = {}

    def load_responses(self, json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                responses = json.load(file)
                print(f"[INFO] ResponseR file loaded successfully: {json_path}")
                return responses.get("exam_data", [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERROR] Unable to load ResponseR file: {e}")
            return []

    def load_responsesDoc(self, json_path2):
            try:
                with open(json_path2, "r", encoding="utf-8") as file:
                    responses = json.load(file)
                    print(f"[INFO] ResponseR doc file loaded successfully: {json_path2}")
                    return responses.get("exam_data", [])
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"[ERROR] Unable to load ResponseR doc file: {e}")
                return []

    def handle_exam_recommendation(self, user_input):
        if not isinstance(self.prev_data, dict):
            print(f"[ERROR] Invalid prev_data format: {self.prev_data}")
            self.prev_data = {}

        if "department" not in self.prev_data or not self.prev_data["department"].strip():
            self.prev_data["department"] = user_input.strip().lower()

            if not self.prev_data.get("department") or self.prev_data["department"].strip() == "":
                return "what is your department?", ["cs", "cs & math", "cs & stat", "cs & phy"]

            return "What is your academic year?", ["freshman (level one)",
                                                   "sophomore (level two)",
                                                   "Junior (level three)",
                                                   "senior (level four)"]

        if "year" not in self.prev_data:
            self.prev_data["year"] = user_input.strip().lower()
            return "What is your semester?", ["one", "two"]

        if "semester" not in self.prev_data:
            self.prev_data["semester"] = user_input.strip().lower()
            return "What is the subject name?", self.get_subject_options()

        if "subject" not in self.prev_data:
            self.prev_data["subject"] = user_input.strip().lower()
            return "Who is the professor?",self.get_professor_options()
        self.prev_data["instructor"]=user_input.strip().lower()

        if ("department" in self.prev_data and "year" in self.prev_data  and
             "semester" in self.prev_data and "subject" in self.prev_data and
            "instructor" in self.prev_data):
            print(self.prev_data)
            return self.get_exam_system()
        else:
            return "sorry the answer not matched with my data ",[]

    def get_subject_options(self):
        subjects = {
            ("freshman (level one)","one"):["saftey","human rights","calculus & integration",
                                "physics","chemistry","statistics"],
            ("freshman (level one)","two"):["calculus & integration 2",
                                "Basic concepts in mathematics","html & css","c++"
                                ,"logic design","english"],
            ("sophomore (level two)", "one"): ["algorithm", "computability",
                                   "oop", "database", "linear algebra", "english"],
            ("sophomore (level two)", "two"): ["data structure", "network", "web programming",
                                   "automata", "graph", "ordinary differential equation"],
            ("Junior (level three)", "one"): ["java", "syntax", "complexity", "operating system",
                                "abstract algebra", "multimedia", "scientific thinking"],
            ("Junior (level three)", "two"): ["scientific research ethics", "combinatorics",
                                "compiler", "graphics", "android", "advanced data base"
                                , "crypto"],
            ("senior (level four)", "one"): ["skills", "artificial intelligence", "parallel",
                                "project", "image processing", "cyber security"
                                , "computational geometry"],
            ("senior (level four)", "two"): ["bioinformatics", "software engineering",
                                "advanced artificial intelligence", "data mining"]
        }
        return subjects.get((self.prev_data.get("year"), self.prev_data.get("semester")), [])

    def get_professor_options(self):
        category_subjects_map = {
            "computer":["oop","data structure", "web programming","network",
                        "operating system","java","android","crypto", "compiler",
                         "graphics", "advanced data base" , "database","multimedia",
                        "bioinformatics", "software engineering",
                        "advanced artificial intelligence", "data mining",
                        "html & css", "c++", "logic design","algorithm", "computability",
                        "automata", "graph","syntax", "complexity", "parallel",
                        "artificial intelligence""image processing", "cyber security",
                        "computational geometry", "combinatorics"],

            "math": [ "calculus & integration","statistics","calculus & integration 2",
                        "Basic concepts in mathematics", "linear algebra",
                        "ordinary differential equation","abstract algebra",
                      "computational geometry"],

            "phy": ["physics"],

            "chem": ["chemistry"],

            "require": ["saftey","human rights","english", "scientific thinking",
                        "scientific research ethics","skills"]
        }
        professor_by_category = {
            "computer":["dr nashwa" ,"dr mohamed fakhry" ,"dr neevin","dr doalat",
                        "dr ghada","dr diaa" ,"dr mohamed hashem" ,"dr azza",
                        "dr hussein" ,"dr howaida"],

            "math": ["dr ayat","dr hany" , "dr manar", "dr ahmed gaber"
                       , "dr samir","dr ahmed el-sonbaty","dr ghada" ,"dr essam"],

            "phy": ["dr heba","dr sayed"],

            "chem": ["dr ayman ayoub" ,"dr mohamed emad"],

            "require": ["dr abdelrahman","dr mohamed"]
        }

        subject = self.prev_data.get("subject", "").strip()
        category = next((cat for cat, subjects in category_subjects_map.items() if subject in subjects), "متطلب")

        return professor_by_category.get(category, [])

    def get_exam_system(self):
        exam_system_response = ""
        exam_format_message = ""

        if not exam_system_response:
            for doctor in self.doctors:
                if self.prev_data["instructor"].lower() in [d.lower() for d in doctor["instructo"]]:
                    professor_name = ', '.join(doctor['instructo']) if isinstance(doctor['instructo'], list) else doctor['instructo']
                    exam_sys = doctor["exam_system"]
                    exam_system_text = ', '.join(exam_sys)
                    exam_system_response = f"Exam system for {professor_name}: \n{exam_system_text}"
                    break
        if not exam_format_message:
            for exam in self.responses:
                if (self.prev_data["department"].lower() in [di.lower() for di in exam["department"]] and
                        self.prev_data["year"].lower() in [y.lower() for y in exam["level"]] and
                        self.prev_data["semester"].lower() in [s.lower() for s in exam["semester"]] and
                        self.prev_data["subject"].lower() in [sub.lower() for sub in exam["subject"]]):

                    exam_format = exam['exam_format']
                    subject_name = ', '.join(exam['subject']) if isinstance(exam['subject'], list) else exam['subject']

                    exam_format_text = ', '.join(exam_format)
                    exam_format_message = f"Exam Format for the subject {subject_name}:\n{exam_format_text}"
                    break

        if not exam_format_message:
                exam_format_message = "No exam data available for this subject."
        if not  exam_system_response:
                exam_system_response="No professor data available for this subject."

        if exam_system_response and exam_format_message:
            self.prev_data.clear()
            return (f"firstly I would like to tell you not to worry,"
                    f" always be reassured that the exams will be good and you will pass."
                    f" As for {exam_format_message}\n\n, {exam_system_response}"), []

        return "No matching exam data or professor information.", []