from Ai.ArabicAi.chattask import ChatTask
from Ai.ArabicAi.Replies.basic_replies import handle_basic_reply
from Ai.ArabicAi.Replies.course_replies import handle_course_reply
from Ai.ArabicAi.Replies.professor_replies import handle_professor_reply
from Ai.ArabicAi.Replies.general_replies import handle_general_reply
import variables
import json

class replyModule:
    def __init__(self, json_path=variables.ResponseDataLocationAr):
        self.load_responses(json_path)

    def load_responses(self, json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                self.data = json.load(file)
            print(f"[INFO] Response file loaded successfully: {json_path}")
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"[ERROR] Couldn't load or parse the response file: {json_path}")
            self.data = {}

    def generate_response(self, reply: list[tuple[ChatTask, ...]]) -> str:
        s = ""
        for r in reply:

            if r[0] in [ChatTask.GreetingTask, ChatTask.UnderstandingTask, ChatTask.askNameTask,
                        ChatTask.ContradactionTask, ChatTask.CheckWellbeingTask, ChatTask.ThanksTask,
                        ChatTask.askHelpingTask, ChatTask.GoodbyeTask, ChatTask.ConfusionTask]:
                s += "\n" + handle_basic_reply(r, self.data)
                
            elif r[0] in [ChatTask.CourseQueryTask,ChatTask.CourseOfProfessor,ChatTask.CourseHours,
                          ChatTask.CourseDegrees,ChatTask.PrerequisiteQueryTask,
                          ChatTask.CourseOfAssistant,ChatTask.DepartmentOfCourse] :
                s += "\n" + handle_course_reply(r, self.data)

            elif r[0] in [ChatTask.ProfessorQueryTask,ChatTask.AssistantTask,ChatTask.HeadOfDepartment,
                          ChatTask.ProfessorOfCourse]:

                s += "\n" + handle_professor_reply(r, self.data)

            else:
                s += "\n" + handle_general_reply(r, self.data)

        return s.strip()
