import json
from Ai.Recommendation.chatTaskR import ChatTaskR
from nltk.corpus import wordnet
import variables

class TaskMapperR:
    def __init__(self, json_path=variables.MapDataLocationRE):
        self.task_definitions = self.load_definitions(json_path)

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

    def convert_to_enum(self, task_name: str) -> ChatTaskR:
        return ChatTaskR[task_name] if task_name in ChatTaskR.__members__ else ChatTaskR.UnknownTask

    def match_for_pos(self, task: ChatTaskR, item_type: str, token: str) -> bool:
        item_list = self.task_definitions[task][item_type]

        for x in item_list:
            if x == token:
                return True
        for x in item_list:
            for synset in wordnet.synsets(token):
                for lemma_name in synset.lemma_names():
                    if lemma_name.lower() == x.lower():
                        return True
        return False
    def MaxMatches(self, task: ChatTaskR, position: list, tokens: list) -> float:
        max_matches = 0
        temp_position = position[:]
        temp_tokens = tokens[:]
        question_pos = self.getPOS("WP", temp_position)
        if question_pos == -1:
            question_pos = self.getPOS("WRB", temp_position)
        if question_pos == -1:
            question_pos = self.getPOS("MD", temp_position)
        if question_pos == -1:
            question_pos = self.getPOS("WDT", temp_position)
        if question_pos == -1:
            question_pos = self.getPOS("V", temp_position)
        question = temp_tokens[question_pos] if question_pos != -1 else None
        question_found = False
        if question and self.match_for_pos(task, "QuestionKeywords", question):
            max_matches += 1
            question_found = True
            temp_tokens.pop(question_pos)
            temp_position.pop(question_pos)
        if question_found:
            verb_pos = self.getPOS("V", temp_position)
            verb = temp_tokens[verb_pos] if verb_pos != -1 else None
            if verb and self.match_for_pos(task, "VerbKeywords", verb):
                max_matches += 2
                temp_tokens.pop(verb_pos)
                temp_position.pop(verb_pos)
        prp_pos = self.getPOS("PRP", temp_position)
        if prp_pos == -1:
            prp_pos = self.getPOS("NNS", temp_position)
        prp = temp_tokens[prp_pos] if prp_pos != -1 else None
        if prp and self.match_for_pos(task, "SubjectKeywords", prp):
            max_matches += 1
            temp_tokens.pop(prp_pos)
            temp_position.pop(prp_pos)
        for token in temp_tokens:
            if self.match_for_pos(task, "ObjectKeywords", token):
                max_matches += 0.2
        return max_matches

    def isModalVerb(self, token: str) -> bool:
        return token in ["be", "do", "have", "will", "can", "could", "shall", "should", "may", "might", "must"]

    def isQuestionTool(self, token: str) -> bool:
        return token in ["what", "where", "when", "who", "whose", "which", "why", "how"]

    def isQuestion(self, tokens: list[str]) -> bool:
        if not len(tokens):
            return False
        if self.isQuestionTool(tokens[0]) or self.isQuestionTool(tokens[-1]):
            return True
        elif self.isModalVerb(tokens[0]):
            return True
        return False

    def getPOS(self, tag: str, pos: list[str]) -> int:
        for i, x in enumerate(pos):
            if x.startswith(tag):
                return i
        return -1
    def mapTokenR(self, tokens: list[list[str]], pos: list[list[str]]) -> list[tuple[ChatTaskR,]]:
        res = list()
        if not tokens or not pos or len(tokens) != len(pos):
            return [(ChatTaskR.UnknownTask, "Invalid input")]
        for i, data in enumerate(tokens):
            if self.isQuestion(data):
                best_task = "UnknownTask"
                max_score = 0
                for task in self.task_definitions.keys():
                    score = self.MaxMatches(task, pos[i], data)
                    print(f"{score} : {task}")
                    if score > max_score:
                        max_score = score
                        best_task = task
                        best_task_enum = self.convert_to_enum(best_task)
                if best_task_enum != ChatTaskR.UnknownTask and max_score >= 1.5:
                    res.append((best_task_enum, data))
                else:
                    res.append((ChatTaskR.UnknownTask,))
            else:
                verbIndex = self.getPOS("VB", pos[i])
                if verbIndex != -1:
                    if data[verbIndex] == "be":
                        if pos[i][verbIndex - 1].startswith("N") and (
                                pos[i][verbIndex + 1].startswith("J") or pos[i][verbIndex + 1].startswith("N") or
                                pos[i][verbIndex + 1].endswith("N")):
                            res.append((ChatTaskR.StoreTask, data[verbIndex - 1], data[verbIndex + 1]))
                else:
                    res.append((ChatTaskR.UnknownTask,))
        if len(res) == 0:
            res.append((ChatTaskR.UnknownTask,))
            return res
        else:
            return res