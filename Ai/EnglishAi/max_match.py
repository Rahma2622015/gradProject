from Ai.EnglishAi.chattask import ChatTask
from Ai.EnglishAi.functionsForMapping import functions
from nltk.corpus import wordnet
import variables
import json
fun=functions()
class match:
    def __init__(self, json_path=variables.MapDataLocationEn):
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


    def match_for_pos(self, task: ChatTask, item_type: str, token: str) -> bool:
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

    def MaxMatches(self, task: ChatTask, position: list, tokens: list) -> float:
        max_matches = 0
        temp_position = position[:]
        temp_tokens = tokens[:]
        question_pos = fun.getPOS("WP", temp_position)
        if question_pos == -1:
            question_pos = fun.getPOS("WRB", temp_position)
        if question_pos == -1:
            question_pos = fun.getPOS("MD", temp_position)
        if question_pos == -1:
            question_pos = fun.getPOS("WDT", temp_position)
        if question_pos == -1:
            question_pos = fun.getPOS("V", temp_position)
        question = temp_tokens[question_pos] if question_pos != -1 else None
        question_found = False
        if question and self.match_for_pos(task, "QuestionKeywords", question):
            max_matches += 1
            question_found = True
            temp_tokens.pop(question_pos)
            temp_position.pop(question_pos)
        if question_found:
            verb_pos = fun.getPOS("V", temp_position)
            verb = temp_tokens[verb_pos] if verb_pos != -1 else None
            if verb and self.match_for_pos(task, "VerbKeywords", verb):
                max_matches += 2
                temp_tokens.pop(verb_pos)
                temp_position.pop(verb_pos)
        prp_pos = fun.getPOS("PRP", temp_position)
        if prp_pos == -1:
            prp_pos = fun.getPOS("NNS", temp_position)
        if prp_pos == -1:
            prp_pos = fun.getPOS("NN", temp_position)
        prp = temp_tokens[prp_pos] if prp_pos != -1 else None
        if prp and self.match_for_pos(task, "SubjectKeywords", prp):
            max_matches += 1
            temp_tokens.pop(prp_pos)
            temp_position.pop(prp_pos)
        for token in temp_tokens:
            if self.match_for_pos(task, "ObjectKeywords", token):
                max_matches += 0.2
        return max_matches