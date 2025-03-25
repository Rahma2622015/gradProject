from Ai.Recommendation.ReplyTaskR import ReplyTaskR
from Data.dataStorage import DataStorage
from Ai.Recommendation.chatTaskR import ChatTaskR


class TaskProcessorRe:

    @staticmethod
    def convert_to_enum(task_name: str) -> ChatTaskR:
        return ChatTaskR[task_name] if task_name in ChatTaskR.__members__ else ChatTaskR.UnknownTask

    def processR(self, tasks: list[tuple[ChatTaskR, list]], data: DataStorage) -> list[tuple[ReplyTaskR, str]]:
        responses = []

        for task in tasks:
            task_enum = task[0]

            if isinstance(task_enum, ChatTaskR):
                if task_enum == ChatTaskR.ExamSystem:
                    responses.append((ReplyTaskR.ExamSystem, ""))
                    print(f"[DEBUG] Task {task_enum} added to responses.")
                else:
                    responses.append((ReplyTaskR.UnknownTask, ""))

        return responses


