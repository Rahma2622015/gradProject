import json
from Data.dataStorage import DataStorage
import variables

class CourseRecommendation:
    def __init__(self, json_path=variables.MapDataLocationEn,
                 json_file=variables.RecomLocation):
        self.json_file = json_file
        self.course_data = self.load_course_data()
        self.storage = DataStorage()
        self.task_definitionsR = self.load_definitions(json_path)

    def load_definitions(self, json_path: str) -> dict:
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                print(f"[INFO] mapR file loaded successfully: {json_path}")
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERROR] Unable to load mapR file: {e}")
            return {}

    def load_course_data(self):
        try:
            with open(self.json_file, "r", encoding="utf-8") as file:
                print(f"[INFO] Course data loaded successfully: {self.json_file}")
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERROR] Unable to load course data: {e}")
            return {}

    def handle_course_recommendation(self, user_input, user_id):
        prev_data = self.storage.get_prev_data(user_id)

        if not isinstance(prev_data, dict):
            print(f"[ERROR] Invalid prev_data format: {prev_data}")
            prev_data = {}

        if "year" not in prev_data or not prev_data["year"].strip():
            print("[DEBUG] Asking for year first")
            self.storage.save_data(user_id, "year", user_input.strip().lower())
            prev_data = self.storage.get_prev_data(user_id)

            if not prev_data.get("year") or prev_data["year"].strip() == "":
                return "What is the year you want to inquire about a subject in?", ["first", "second", "third",
                                                                                    "fourth"]

            return "What is the semester you want to inquire about a subject in?", ["one", "two"]

        if "semester" not in prev_data or not prev_data["semester"].strip():
            print("[DEBUG] Asking for semester next")

            if user_input.strip().lower() == prev_data["year"]:
                return "Please enter a valid semester (one or two), not the year again.", ["one", "two"]

            self.storage.save_data(user_id, "semester", user_input.strip().lower())
            prev_data = self.storage.get_prev_data(user_id)

            if not prev_data.get("semester") or prev_data["semester"].strip() == "":
                return "What is the semester you want to inquire about a subject in?", ["one", "two"]

        courses = self.get_subject_options(prev_data)
        print(f"[DEBUG] Courses found: {courses}")

        if not courses:
            return "Sorry, no courses found for the selected year and semester.", []

        if "subject" not in prev_data or not prev_data["subject"].strip():
            print("[DEBUG] Asking for subject")

            if user_input.strip().lower() not in [course.lower() for course in courses]:
                return "Please enter a valid subject from the available options:", courses

            self.storage.save_data(user_id, "subject", user_input.strip().lower())
            prev_data = self.storage.get_prev_data(user_id)
            print(f"[DEBUG] Subject after storing: {prev_data.get('subject')}")

            return self.evaluate_course_suitability(prev_data, user_id)

    def get_subject_options(self, prev_data):
        subjects = {
            ("first", "one"): ["calculus & integration", "physics"
                , "chemistry", "statistics"],
            ("first", "two"): ["c++", "html & css", "logic design"],
            ("second", "one"): ["algorithm", "computability", "oop", "database"
                , "linear algebra", "english"],
            ("second", "two"): ["data structure", "network", "web programming"
                , "automata", "graph", "ordinary differential equation"],
            ("third", "one"): ["java", "syntax", "complexity", "operating system"
                , "abstract algebra", "multimedia", "scientific thinking"],
            ("third", "two"): ["scientific research ethics", "combinatorics", "compiler"
                , "graphics", "android", "advanced data base", "crypto"],
            ("fourth", "one"): ["skills", "artificial intelligence", "parallel", "project"
                , "image processing", "cyber security", "Computational geometry"],
            ("fourth", "two"): ["bioinformatics", "software engineering", "project"
                , "advanced artificial intelligence", "data mining"]
        }
        return subjects.get((prev_data.get("year"), prev_data.get("semester")), [])

    def find_course(self, course_name, year, sem):
        print(year, sem)
        for y in self.course_data:
            if y.lower() == year.lower():
                for term in self.course_data[y]:
                    if term.lower() == sem.lower():
                        courses = self.course_data[y][term]
                        print("Courses found by find_course:", courses.keys())
                        for subject in courses:
                            if subject.lower() == course_name.lower():
                                return courses[subject]
                        print(f"Course not found: {course_name}")
                        return None  # Ensure to handle the missing course case
        return None

    def evaluate_course_suitability(self, prev_data, user_id, user_input=None):
        course_name = prev_data["subject"]
        year = prev_data["year"]
        semester = prev_data["semester"]
        print(course_name)

        # Find the course data
        course_data = self.find_course(course_name, year, semester)

        if course_data is None:
            return "Sorry, I don’t have information about this course. Try another one.", []

        questions = course_data.get("questions", {})
        print(f"que: {questions}")
        pass_threshold = course_data.get("pass_threshold", 0)

        suitability_data = prev_data.get("suitability_data", {
            "total_score": 0,
            "max_score": sum(max(questions[q].values()) for q in questions) if questions else 0,
            "current_question_index": 0,
            "questions": list(questions.keys()) if questions else []
        })

        questions = suitability_data["questions"]
        current_index = suitability_data["current_question_index"]

        # If there are no questions, handle this case
        if not questions:
            return "No questions available for this course.", []

        # If there is no user input, ask the first question
        if user_input is None:
            suitability_data["current_question_index"] = 0  # reset index to 0 for new data
            self.storage.save_data(user_id, "suitability_data", suitability_data)

            current_question = questions[current_index]

            if current_question not in questions:
                return "Error: invalid question.", []
            options = list(course_data["questions"][current_question].keys())
            print(f"[DEBUG] Index before increment: {suitability_data['current_question_index']}")
            suitability_data["current_question_index"] += 1
            print(f"[DEBUG] Index after increment: {suitability_data['current_question_index']}")
            return f"{current_question}", options

        last_question = questions[current_index]

        if last_question not in course_data["questions"]:
            return "Error: invalid question.", []

        question_options = course_data["questions"][last_question]

        if user_input in question_options:
            suitability_data["total_score"] += question_options[user_input]

        current_index = suitability_data["current_question_index"]

        # Check if all questions have been answered
        if current_index >= len(questions):
            suitability_percentage = (suitability_data["total_score"] / suitability_data["max_score"]) * 100
            self.storage.clear_data(user_id, keep_task=True)
            print(f"Suitability Score: {suitability_percentage:.2f}%")

            if suitability_percentage >= pass_threshold:
                return f"{course_name} seems to be a great fit for you!", []
            elif 50 <= suitability_percentage < pass_threshold:
                return f"{course_name} is suitable, but you may need to put in extra effort!", []
            else:
                return f"{course_name} might not be the best choice for you. Consider another option.", []

        # If there are more questions, ask the next one
        prev_data["suitability_data"] = suitability_data
        self.storage.save_data(user_id, "prev_data", prev_data)

        next_question = questions[current_index]

        if next_question not in course_data["questions"]:
            return "Error: invalid question.", []

        options = list(course_data["questions"][next_question].keys())

        return f"{next_question}", options
