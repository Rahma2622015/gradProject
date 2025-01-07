from Ai.chattask import ChatTask
from nltk.corpus import wordnet
from Ai.MapData import TaskDefinitions

class TaskMapper:
    def __init__(self):
        self.task_definitions = TaskDefinitions().get_definitions()


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
        if prp_pos==-1:
            prp_pos =self.getPOS("NNS",temp_position)
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
        return token in ["be", "do", "have","will","can", "could", "shall", "should", "may", "might", "must"]

    def isQuestionTool(self, token: str) -> bool:
        return token in ["what", "where", "when", "who", "whose", "which", "why", "how"]

    def isGreetingTool(self, token: str) -> bool:
        greetings = [
            "hi", "hola", "hello", "hey",
            "morning", "evening", "afternoon",
            "greetings", "howdy"
        ]
        return any(greet in token for greet in greetings)

    def isThanksTool(self, token: str) -> bool:
        thanks_words = [
            "thanks", "thank", "thank ", "thx", "ty"
            , "appreciate ", "cheers", "grateful","thanks a lot","thanks so mush","thanks for help"
        ]
        return any(thank in token for thank in thanks_words)

    def isConfusionTool(self, token: str) -> bool:
        confusion = [ "huh", "confuse", "explain"]
        return any(confused in token for confused in confusion)

    def isQuestion(self, tokens: list[str]) -> bool:
        if not len(tokens):
            return False
        if self.isQuestionTool(tokens[0]) or self.isQuestionTool(tokens[-1]):
            return True
        elif self.isModalVerb(tokens[0]):
            return True
        return False

    def isGoodbyeTool(self, token: str) -> bool:
        keywords = ["goodbye", "bye", "later", "see you", "take care", "later",
                    "catch", "later", " again", "have a good one",
                   "peace", "until", "next" ,"time", "adieu", "godspeed", "again",
                    "night", " nice day", "best", "safe"]
        return any(g in token for g in keywords)
    def getPOS(self, tag: str, pos: list[str]) -> int:
        for i, x in enumerate(pos):
            if x.startswith(tag):
                return i
        return -1

    def mapToken(self, tokens: list[list[str]], pos: list[list[str]]) -> list[tuple[ChatTask,]]:
        res = list()
        if not tokens or not pos or len(tokens) != len(pos):
            return [(ChatTask.UnknownTask, "Invalid input")]
        for i, data in enumerate(tokens):
            if self.isQuestion(data):
                best_task = ChatTask.UnknownTask
                max_score = 0
                for task in self.task_definitions.keys():
                    score = self.MaxMatches(task, pos[i], data)
                    print(f"{score} : {task}")
                    if score > max_score:
                        max_score = score
                        best_task = task
                if best_task != ChatTask.UnknownTask:
                 if max_score >=1.5:
                    res.append((best_task, data))
                else:
                    res.append((ChatTask.UnknownTask,))
            elif self.isGreetingTool(data):
                res.append((ChatTask.GreetingTask, "name"))
            elif self.isThanksTool(data):
                res.append((ChatTask.ThanksTask, ""))
            elif self.isGoodbyeTool(data):
                res.append((ChatTask.GoodbyeTask, ""))
            elif self.isConfusionTool(data):
                res.append((ChatTask.ConfusionTask, ""))
            else:
                verbIndex = self.getPOS("VB", pos[i])
                if verbIndex != -1:
                    if data[verbIndex] == "be":
                        if pos[i][verbIndex - 1].startswith("N") and (
                                pos[i][verbIndex + 1].startswith("J") or pos[i][verbIndex + 1].startswith("N") or pos[i][verbIndex +1].endswith("N")):
                            res.append((ChatTask.StoreTask, data[verbIndex - 1], data[verbIndex + 1]))
                else:
                    res.append((ChatTask.UnknownTask,))
        if len(res) == 0:
            res.append((ChatTask.UnknownTask,))
            return res
        else:
            return res