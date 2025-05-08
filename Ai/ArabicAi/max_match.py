import  json
from Ai.ArabicAi.chattask import ChatTask
import difflib
import variables


class match:
    def __init__(self,json_path=variables.MapDataLocationAr):
        self.task_definitions = self.load_definitions(json_path)

    def load_definitions(self, json_path: str) -> dict:
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: File {json_path} not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Failed to parse JSON from {json_path}.")
            return {}

    def convert_to_enum(self, task_name: str) -> ChatTask:
        try:
            task_enum_name = task_name.replace("ChatTask.", "")
            return ChatTask[task_enum_name] if task_enum_name in ChatTask.__members__ else ChatTask.UnknownTask
        except KeyError:
            print(f"Warning: Task '{task_name}' not found in ChatTask!")
            return ChatTask.UnknownTask

    def match_for_pos(self, task: ChatTask, item_type: str, token: str) -> bool:
        if not token:
            return False

        task_name = task if isinstance(task, str) else f"ChatTask.{task.name}"
        item_list = self.task_definitions.get(task_name, {}).get(item_type, [])

        for x in item_list:
            if token == x:
                return True

            similarity_ratio = difflib.SequenceMatcher(None, token, x).ratio()
            if similarity_ratio > 0.85:
                return True

        return False

    def getPOS(self, tags: list[str], pos: list[str]) -> int:
        for i, x in enumerate(pos):
            if isinstance(x, str) and any(x.startswith(tag) for tag in tags):
                return i
        return -1

    def MaxMatches(self, task: ChatTask, position: list, tokens: list) -> float:
        max_matches = 0
        temp_position = position[:]
        temp_tokens = tokens[:]


        question_pos = self.getPOS(["DET", "NOUN", "PART", "CCONJ", "ADJ", "AUX","INTJ"], temp_position)

        question = temp_tokens[question_pos] if question_pos != -1 else None
        question_found = False

        if self.match_for_pos(task, "اداة_استفهام", question):
            max_matches += 1
            question_found = True
            temp_tokens.pop(question_pos)
            temp_position.pop(question_pos)

        if question_found:
            verb_pos = self.getPOS(["VERB", "AUX","PRON"], temp_position)
            if verb_pos != -1:
                verb = temp_tokens[verb_pos]
                if self.match_for_pos(task, "فعل", verb):
                    max_matches += 2
                    temp_tokens.pop(verb_pos)
                    temp_position.pop(verb_pos)


        prp_pos = self.getPOS(["PRON", "NOUN"], temp_position)
        if prp_pos != -1:
            prp = temp_tokens[prp_pos]
            if self.match_for_pos(task, "فاعل", prp):
                max_matches += 1
                temp_tokens.pop(prp_pos)
                temp_position.pop(prp_pos)


        for token in temp_tokens:
            if self.match_for_pos(task, "مفعول", token):
                max_matches += 0.2

        return max_matches

    def classify_task(self, tokens: list[str]) -> ChatTask:
        for task_name, task_data in self.task_definitions.items():
            clean_task_name = task_name.replace("ChatTask.", "")
            for item_type, keywords in task_data.items():
                for token in tokens:
                    if any(word == token for word in keywords):
                        print(self.convert_to_enum(clean_task_name))
                        return self.convert_to_enum(clean_task_name)

        return ChatTask.UnknownTask
