import json
from random import choice
from Ai.EnglishAi.chattask import ChatTask
import variables

class ReplyModule:
    def __init__(self, json_path =variables.ResponseDataLocationEn):
        self.load_responses(json_path)

    def load_responses(self, json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                self.data = json.load(file)
            print(f"[INFO] Response file loaded successfully: {json_path}")
        except FileNotFoundError:
            print(f"[ERROR] Response file not found: {json_path}")
            self.data = {}
        except json.JSONDecodeError:
            print(f"[ERROR] Invalid JSON format in: {json_path}")
            self.data = {}

    def generate_response(self, reply: list[tuple[ChatTask, ...]]) -> tuple[str, list]:
        s = ""
        for r in reply:
            if r[0] == ChatTask.GreetingTask:
                s += "\n" + choice(self.data.get("Greeting", [])).format(x=r[1])
            elif r[0] == ChatTask.UnderstandingTask:
                s += "\n" + choice(self.data.get("Understanding", [])).format(x=r[2])
            elif r[0] == ChatTask.AskNameTask:
                s += "\n" + choice(self.data.get("replay_name", [])).format(x=r[1])
            elif r[0] == ChatTask.ContradictionTask:
                s += "\n" + choice(self.data.get("Contradiction", [])).format(y=r[2])
            elif r[0] == ChatTask.CheckWellbeingTask:
                s += "\n" + choice(self.data.get("CheckWellbeing", []))
            elif r[0] == ChatTask.ThanksTask:
                s += "\n" + choice(self.data.get("ThanksReplies", []))
            elif r[0] == ChatTask.HelpTask:
                s += "\n" + choice(self.data.get("askhelp", []))
            elif r[0] == ChatTask.GoodbyeTask:
                s += "\n" + choice(self.data.get("Goodbye", []))
            elif r[0] == ChatTask.ConfusionTask:
                s += "\n" + choice(self.data.get("ConfusionReplies", []))
            # end trivial
            elif r[0] == ChatTask.TypesOfProgramsTask:
                s += "\n" + choice(self.data.get("Programs", []))
            elif r[0] == ChatTask.MathTask:
                s += "\n" + choice(self.data.get("Math", []))
            elif r[0] == ChatTask.ExternalCoursesTask:
                s += "\n" + choice(self.data.get("ExternalCourses", []))
            elif r[0] == ChatTask.DifficultyTask:
                s += "\n" + choice(self.data.get("Difficulty", []))
            elif r[0] ==ChatTask.HighGpaTask:
                s += "\n" + choice(self.data.get("HighGpa", []))
            elif r[0] == ChatTask.MaterialsTypeTask:
                s += "\n" + choice(self.data.get("MaterialType", []))
            elif r[0] == ChatTask.ChooseDepartmentTask:
                s += "\n" + choice(self.data.get("chooseDepartment", []))
            elif r[0] == ChatTask.AcademicAdvisorTask:
                s += "\n" + choice(self.data.get("AcademicAdvisorTask", []))
            elif r[0] == ChatTask.ClassificationTask:
                s += "\n" + choice(self.data.get("Classification", []))
            elif r[0] == ChatTask.CreditHoursTask:
                s += "\n" + choice(self.data.get("CreditHours", []))
            elif r[0] == ChatTask.GraduationTask:
                s += "\n" + choice(self.data.get("Graduation", []))
            elif r[0] == ChatTask.EnrollmentTask:
                s += "\n" + choice(self.data.get("Enrollment", []))
            elif r[0] == ChatTask.ProfessorQueryTask:
                professor_name = r[1] if len(r) > 1 and r[1] else "Professor name not provided"
                professor_info = r[2] if len(r) > 2 and r[2] else "No Information Available"
                s += "\n" + choice(self.data.get("ProfessorQueryTask", [])).format(x=professor_name, y=professor_info)

            elif r[0] == ChatTask.CourseQueryTask:
                s += "\n" + choice(self.data.get("CourseQueryTask", [])).format(x=r[1], y=r[2])
            else:
                s += "\n" + choice(self.data.get("Unknown", []))

        return s.strip(),[]