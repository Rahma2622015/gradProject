import json
from Ai.EnglishAi.chattask import ChatTask
import variables

class MappingTrivial:
    def __init__(self, json_path=variables.MapDataLocationEn):
        self.taskDefinitions = self.load_definitions(json_path)

    def load_definitions(self, json_path: str) -> dict:
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                print(f"[INFO] Map trival file loaded successfully: {json_path}")
                return json.load(file)
        except FileNotFoundError:
            print(f"[ERROR] map trival file not found: {json_path}")
            return {}
        except json.JSONDecodeError:
            print(f"[ERROR] Invalid JSON format in: {json_path}")
            return {}

    def convert_to_enum(self, task_name: str) -> ChatTask:
        return ChatTask.get(task_name, ChatTask.UnknownTask)

    def isGreetingTool(self, token: str) -> bool:
        greetings = {"hi", "hola", "hello", "hey", "morning", "evening", "afternoon", "greetings", "howdy"}
        return token.lower() in greetings

    def isThanksTool(self, token: str) -> bool:
        thanks_words = {"thanks", "thank", "thx", "ty", "appreciate", "cheers", "grateful",
                        "thanks a lot", "thanks so much", "thanks for help"}
        return token.lower() in thanks_words

    def isConfusionTool(self, token: str) -> bool:
        confusion_words = {"huh", "confuse", "explain"}
        return token.lower() in confusion_words

    def isGoodbyeTool(self, token: str) -> bool:
        goodbye_words = {"goodbye", "bye", "later", "see you", "take care", "catch you later",
                         "have a good one", "peace", "until next time", "adieu", "godspeed", "good night"}
        return token.lower() in goodbye_words

    def getPOS(self, tag: str, pos: list[str]) -> int:
        return next((i for i, x in enumerate(pos) if x.startswith(tag)), -1)

    def mapToken(self, tokens: list[list[str]], pos: list[list[str]]) -> list[tuple[ChatTask,]]:
        res = []
        if not tokens or not pos or len(tokens) != len(pos):
            return [(ChatTask.UnknownTask, "Invalid input")]

        for i, sentence in enumerate(tokens):
            if any(self.isGreetingTool(word) for word in sentence):
                res.append((ChatTask.GreetingTask, "name"))
            elif any(self.isThanksTool(word) for word in sentence):
                res.append((ChatTask.ThanksTask, ""))
            elif any(self.isGoodbyeTool(word) for word in sentence):
                res.append((ChatTask.GoodbyeTask, ""))
            elif any(self.isConfusionTool(word) for word in sentence):
                res.append((ChatTask.ConfusionTask, ""))
            else:
                verbIndex = self.getPOS("VB", pos[i])
                if verbIndex != -1 and sentence[verbIndex] == "be":
                    if pos[i][verbIndex - 1].startswith("N") and (
                            pos[i][verbIndex + 1].startswith("J") or pos[i][verbIndex + 1].startswith("N")):
                        res.append((ChatTask.StoreTask, sentence[verbIndex - 1], sentence[verbIndex + 1]))
                else:
                    res.append((ChatTask.UnknownTask,))

        return res if res else [(ChatTask.UnknownTask,)]
