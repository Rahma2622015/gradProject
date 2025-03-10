import json
from random import choice
from Ai.ReplyTask import ReplyTask

class ReplyModule:
    def __init__(self, json_path="response.json"):
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

    def generate_response(self, reply: list[tuple[ReplyTask, ...]]) -> str:
        s = ""
        for r in reply:
            if r[0] == ReplyTask.Greeting:
                s += "\n" + choice(self.data.get("Greeting", [])).format(x=r[1])
            elif r[0] == ReplyTask.UnderstandingTask:
                s += "\n" + choice(self.data.get("Understanding", [])).format(x=r[2])
            elif r[0] == ReplyTask.AskName:
                s += "\n" + choice(self.data.get("replay_name", [])).format(x=r[1])
            elif r[0] == ReplyTask.ContradictionTask:
                s += "\n" + choice(self.data.get("Contradiction", [])).format(y=r[2])
            elif r[0] == ReplyTask.CheckWellbeing:
                s += "\n" + choice(self.data.get("CheckWellbeing", []))
            elif r[0] == ReplyTask.Thanks:
                s += "\n" + choice(self.data.get("ThanksReplies", []))
            elif r[0] == ReplyTask.Help:
                s += "\n" + choice(self.data.get("askhelp", []))
            elif r[0] == ReplyTask.Goodbye:
                s += "\n" + choice(self.data.get("Goodbye", []))
            elif r[0] == ReplyTask.Confusion:
                s += "\n" + choice(self.data.get("ConfusionReplies", []))
            # end trivial
            elif r[0] == ReplyTask.TypesOfPrograms:
                s += "\n" + choice(self.data.get("Programs", []))
            elif r[0] == ReplyTask.Math:
                s += "\n" + choice(self.data.get("Math", []))
            elif r[0] == ReplyTask.ExternalCourses:
                s += "\n" + choice(self.data.get("ExternalCourses", []))
            elif r[0] == ReplyTask.Difficulty:
                s += "\n" + choice(self.data.get("Difficulty", []))
            elif r[0] == ReplyTask.HighGpa:
                s += "\n" + choice(self.data.get("HighGpa", []))
            elif r[0] == ReplyTask.MaterialsType:
                s += "\n" + choice(self.data.get("MaterialType", []))
            elif r[0] == ReplyTask.ChooseDepartment:
                s += "\n" + choice(self.data.get("chooseDepartment", []))
            elif r[0] == ReplyTask.AcademicAdvisorTask:
                s += "\n" + choice(self.data.get("AcademicAdvisorTask", []))
            elif r[0] == ReplyTask.ClassificationTask:
                s += "\n" + choice(self.data.get("Classification", []))
            elif r[0] == ReplyTask.CreditHours:
                s += "\n" + choice(self.data.get("CreditHours", []))
            elif r[0] == ReplyTask.Graduation:
                s += "\n" + choice(self.data.get("Graduation", []))
            elif r[0] == ReplyTask.Enrollment:
                s += "\n" + choice(self.data.get("Enrollment", []))
            else:
                s += "\n" + choice(self.data.get("Unknown", []))

        return s.strip()
