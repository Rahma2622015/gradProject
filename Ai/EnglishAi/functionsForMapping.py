from Ai.EnglishAi.chattask import ChatTask
class functions:
    def isExclamation(self, token: str) -> bool:
        exclamations = {"wow", "amazing", "incredible", "unbelievable", "awesome", "fantastic"}
        return token.lower() in exclamations

    def isLikeOrLove(self, token: str) -> bool:
        like_love_words = {"like", "love", "adore", "enjoy", "appreciate"}
        return token.lower() in like_love_words

    def isNegative(self, token: str) -> bool:
        negative_words = {
            "sad", "angry", "upset", "depressed",
            "frustrated", "anxious", "hopeless",
            "miserable", "lonely", "hurt", "regret",
            "angry", "annoyed", "disappointed",
            "guilty", "hopeless", "terrible", "worse",
            "down", "helpless",
            "stressed", "sick", "confused", "tired"
        }
        return token.lower() in negative_words

    def isAffirmation(self, token: str) -> bool:
        affirmations = {"yes", "definitely", "sure", "absolutely", "certainly","okay"}
        return token.lower() in affirmations

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

    def convert_to_enum(self, task_name: str) -> ChatTask:
        return ChatTask[task_name] if task_name in ChatTask.__members__ else ChatTask.UnknownTask