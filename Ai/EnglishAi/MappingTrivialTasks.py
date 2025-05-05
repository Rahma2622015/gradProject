import json
from Ai.EnglishAi.chattask import ChatTask
import variables
from Ai.EnglishAi.functionsForMapping import functions

f=functions()

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


    def mapToken(self, tokens: list[list[str]], pos: list[list[str]]) -> list[tuple[ChatTask,]]:
        res = []
        if not tokens or not pos or len(tokens) != len(pos):
            return [(ChatTask.UnknownTask, "Invalid input")]

        for i, sentence in enumerate(tokens):
            if any(f.isGreetingTool(word) for word in sentence):
                res.append((ChatTask.GreetingTask, "name"))
            elif any(f.isThanksTool(word) for word in sentence):
                res.append((ChatTask.ThanksTask, ""))
            elif any(f.isGoodbyeTool(word) for word in sentence):
                res.append((ChatTask.GoodbyeTask, ""))
            elif any(f.isConfusionTool(word) for word in sentence):
                res.append((ChatTask.ConfusionTask, ""))
            else:
                verbIndex = f.getPOS("VB", pos[i])
                if verbIndex != -1 and sentence[verbIndex] == "be":
                    if pos[i][verbIndex - 1].startswith("N") and (
                            pos[i][verbIndex + 1].startswith("J") or pos[i][verbIndex + 1].startswith("N")):
                        res.append((ChatTask.StoreTask, sentence[verbIndex - 1], sentence[verbIndex + 1]))
                else:
                    res.append((ChatTask.UnknownTask,))
        print("mappingTask:",res)
        return res if res else [(ChatTask.UnknownTask,)]