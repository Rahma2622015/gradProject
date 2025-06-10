import json

from Ai.ArabicAi.Mapping import fun
from Ai.ArabicAi.chattask import ChatTask
from Ai.ArabicAi.SentenceSimilarity import SentenceSimilarity
from endPoints.ai_config_endpoints import load_ai_config
import variables

class SemanticTaskMapperArabic:
    def __init__(self, json_path=variables.MapData2LocationAr):
        self.similarity = SentenceSimilarity()
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

    @property
    def config(self):
        return load_ai_config()

    @property
    def threshold(self):
        return self.config.get("threshold", 0.5)

    def mapToken(self, tokens: list[list[str]], pos: list[list[str]]) -> list[tuple[ChatTask,]]:
        res = list()
        if not tokens or not pos or len(tokens) != len(pos):
            return [(ChatTask.UnknownTask, "Invalid input")]

        for i, sentence in enumerate(tokens):
            if any(fun.isGreetingTool(word) for word in sentence):
                res.append((ChatTask.GreetingTask, ""))
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
                #جديد
            #elif any(fun.isHelpTool(word) for word in sentence):
                #res.append((ChatTask.HelpTask, ""))
                #continue

            sentence_text = " ".join(sentence)
            best_task = None
            best_score = 0.0

            for task, task_examples in self.task_definitions.items():
                for task_example in task_examples:
                    score_tuple = self.similarity.get_similarity(sentence_text, task_example)
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
