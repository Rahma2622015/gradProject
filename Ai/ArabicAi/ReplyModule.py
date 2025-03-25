import json
from random import choice
from Ai.ArabicAi.chattask import ChatTask
import variables

class replyModule:
    def __init__(self, json_path = variables.ResponseDataLocationAr):
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

    def generate_response(self, reply: list[tuple[ChatTask, ...]]) -> str:
        s = ""
        for r in reply:
            if r[0] == ChatTask.GreetingTask:
                s += "\n" + choice(self.data.get("Greeting", [])).format(x=r[1])
            elif r[0] == ChatTask.UnderstandingTask:
                s += "\n" + choice(self.data.get("Understanding", [])).format(x=r[2])
            elif r[0] == ChatTask.askNameTask:
                s += "\n" + choice(self.data.get("replay_name", [])).format(x=r[1])
            elif r[0] == ChatTask.ContradactionTask:
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
            elif r[0] == ChatTask.HighGpaTask:
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
            else:
                s += "\n" + choice(self.data.get("Unknown", []))

        return s.strip()