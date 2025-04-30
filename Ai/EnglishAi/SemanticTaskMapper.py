import json
from Ai.EnglishAi.chattask import ChatTask
from Ai.EnglishAi.SentenceSimilarity import SentenceSimilarity
from endPoints.ai_config_endpoints import load_ai_config
import variables

class SemanticTaskMapper:
    def __init__(self, json_path=variables.MapData2LocationEn):
        self.similarity = SentenceSimilarity()
        self.task_definitions = self.load_definitions(json_path)


    @property
    def config(self):
        return load_ai_config()

    @property
    def threshold(self):
        return self.config.get("threshold", 0.5)

    def load_definitions(self, json_path: str) -> dict:
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                print(f"[INFO] map file loaded successfully: {json_path}")
                return json.load(file)
        except FileNotFoundError:
            print(f"[ERROR] map file not found: {json_path}")
            return {}
        except json.JSONDecodeError:
            print(f"[ERROR] Invalid JSON format in: {json_path}")
            return {}

    def convert_to_enum(self, task_name: str) -> ChatTask:
        return ChatTask[task_name] if task_name in ChatTask.__members__ else ChatTask.UnknownTask

    def mapToken(self, tokens: list[list[str]], pos: list[list[str]]) -> list[tuple[ChatTask,]]:
        res = list()
        if not tokens or not pos or len(tokens) != len(pos):
            return [(ChatTask.UnknownTask, "Invalid input")]

        for i, data in enumerate(tokens):
            sentence = " ".join(data)
            best_task = None
            best_score = 0.0

            for task, examples in self.task_definitions.items():
                for example in examples:
                    score_tuple = self.similarity.get_similarity(sentence, example)
                    score = score_tuple[0]

                    if score > best_score:
                        best_score = score
                        best_task = task

            best_task_enum = self.convert_to_enum(best_task) if best_task else ChatTask.UnknownTask

            if best_task_enum != ChatTask.UnknownTask and best_score >= self.threshold:
                res.append((best_task_enum, data, pos[i]))
            else:
                res.append((ChatTask.UnknownTask,))

        return res





