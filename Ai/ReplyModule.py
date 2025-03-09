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
        if not reply:
            print("[WARNING] No task received for generating a response.")
            return "Sorry, I didn't understand your request."

        print(f"[DEBUG] Received tasks: {reply}")

        response_text = ""

        response_mapping = {
            ReplyTask.Greeting.name: self.data.get("Greeting", []),
            ReplyTask.UnderstandingTask.name: self.data.get("Understanding", []),
            ReplyTask.AskName.name: self.data.get("replay_name", []),
            ReplyTask.ContradictionTask.name: self.data.get("Contradiction", []),
            ReplyTask.CheckWellbeing.name: self.data.get("CheckWellbeing", []),
            ReplyTask.Thanks.name: self.data.get("ThanksReplies", []),
            ReplyTask.Help.name: self.data.get("askhelp", []),
            ReplyTask.Goodbye.name: self.data.get("Goodbye", []),
            ReplyTask.Confusion.name: self.data.get("ConfusionReplies", []),
            ReplyTask.TypesOfPrograms.name: self.data.get("Programs", []),
            ReplyTask.Math.name: self.data.get("Math", []),
            ReplyTask.ExternalCourses.name: self.data.get("ExternalCourses", []),
            ReplyTask.Difficulty.name: self.data.get("Difficulty", []),
            ReplyTask.HighGpa.name: self.data.get("HighGpa", []),
            ReplyTask.MaterialsType.name: self.data.get("MaterialType", []),
            ReplyTask.ChooseDepartment.name: self.data.get("chooseDepartment", []),
            ReplyTask.AcademicAdvisorTask.name: self.data.get("AcademicAdvisorTask", []),
            ReplyTask.ClassificationTask.name: self.data.get("Classification", []),
            ReplyTask.CreditHours.name: self.data.get("CreditHours", []),
            ReplyTask.Graduation.name: self.data.get("Graduation", []),
            ReplyTask.Enrollment.name: self.data.get("Enrollment", []),
        }
        for r in reply:
            task_enum = r[0]
            task_string = task_enum.name if isinstance(task_enum, ReplyTask) else "UnknownTask"
            task_params = r[1:] if len(r) > 1 else []

            response_list = response_mapping.get(task_string, self.data.get("Unknown", []))
            if response_list:
                print(f"[INFO] Found responses for task {task_string}: {response_list}")
                formatted_response = choice(response_list).format(x=task_params[0] if task_params else "")
                response_text += "\n" + formatted_response
            else:
                print(f"[WARNING] No responses available for task {task_string} in JSON!")

        response_text = response_text.strip()

        print(f"[DEBUG] Final response: {response_text if response_text else 'No suitable response found.'}")

        return response_text if response_text else "Sorry, I can't respond to that."
