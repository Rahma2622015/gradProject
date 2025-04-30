import json

from Ai.ArabicAi.Mapping import fun
from Ai.ArabicAi.chattask import ChatTask
from Ai.ArabicAi.ArSementicModuel import SentenceSimilarity
import variables

class SemanticTaskMapperArabic:
    def __init__(self, json_path=variables.MapData2LocationAr):
        self.similarity = SentenceSimilarity()
        self.threshold = 0.5
        self.task_definitions = self.load_definitions(json_path)

    def load_definitions(self, json_path: str) -> dict:
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Can't found arabic file ! {json_path}")
            return {}
        except json.JSONDecodeError:
            return {}

    def convert_to_enum(self, task_name: str) -> ChatTask:
        return ChatTask[task_name] if task_name in ChatTask.__members__ else ChatTask.UnknownTask

    def mapToken(self, tokens: list[list[str]], pos: list[list[str]]) -> list[tuple[ChatTask,]]:
        res = list()
        if not tokens or not pos or len(tokens) != len(pos):
            return [(ChatTask.UnknownTask, "Invalid input")]

        for i, sentence in enumerate(tokens):
            if any(fun.isGreetingTool(word) for word in sentence):
                name_value = ""
                for j, word in enumerate(sentence):
                    if word == "اسم":
                        if j + 1 < len(sentence):
                            name_value = sentence[j + 1]
                        break
                    elif word in ["أنا", "انا"]:
                        if j + 1 < len(sentence) and sentence[j + 1] != "اسم":
                            name_value = sentence[j + 1]
                        elif j + 2 < len(sentence) and sentence[j + 1] == "اسم":
                            name_value = sentence[j + 2]
                        break

                res.append((ChatTask.GreetingTask, name_value))
                if name_value:
                    res.append((ChatTask.StoreTask, "اسم", name_value))
                continue
            elif any(fun.isThanksTool(word) for word in sentence):
                res.append((ChatTask.ThanksTask, ""))
                continue

            elif any(fun.isGoodbyeTool(word) for word in sentence):
                res.append((ChatTask.GoodbyeTask, ""))
                continue

            elif any(fun.isConfusionTool(word) for word in sentence):
                res.append((ChatTask.ConfusionTask, ""))
                continue



            sentence_text = " ".join(sentence)
            best_task = None
            best_score = 0.0

            for task, examples in self.task_definitions.items():
                for example in examples:
                    score_tuple = self.similarity.get_similarity(sentence_text, example)
                    score = score_tuple[0]

                    if score > best_score:
                        best_score = score
                        best_task = task

            best_task_enum = self.convert_to_enum(best_task) if best_task else ChatTask.UnknownTask

            if best_task_enum != ChatTask.UnknownTask and best_score >= self.threshold:
                res.append((best_task_enum, sentence, pos[i]))
            else:
                res.append((ChatTask.UnknownTask,))

        return res
