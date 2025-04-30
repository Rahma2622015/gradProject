import json
from random import choice
from Ai.EnglishAi.chattask import ChatTask
import variables

from Ai.EnglishAi.Replies.reply_basic import handle_basic_tasks
from Ai.EnglishAi.Replies .reply_general import handle_general_tasks
from Ai.EnglishAi.Replies .reply_professor import handle_professor_tasks
from Ai.EnglishAi.Replies .reply_course import handle_course_tasks

class ReplyModule:
    def __init__(self, json_path=variables.ResponseDataLocationEn):
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
            for handler in (handle_basic_tasks, handle_general_tasks, handle_professor_tasks, handle_course_tasks):
                result = handler(r, self.data)
                if result:
                    s += "\n" + result
                    break
            else:
                s += "\n" + choice(self.data.get("Unknown", []))
        return s.strip(), []
