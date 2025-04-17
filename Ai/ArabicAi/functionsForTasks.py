class func:

    def isModalVerb(self, token: str) -> bool:
        return token in ["يكون", "يفعل", "لديه", "سوف", "يستطيع", "يمكن", "قد", "يجب", "ينبغي", "ربما"]

    def isQuestionTool(self, token: str) -> bool:
        return token in ["ما", "ماذا", "أين", "متى", "من", "لمن", "أي", "لماذا", "كيف","هل"]

    def isGreetingTool(self, token: str) -> bool:
        greetings = ["اهلا", "مرحبا" ,"أهلين" ,"بونجور","أهلا","هاي"]
        return any(greet in token for greet in greetings)

    def isThanksTool(self, token: str) -> bool:
        thanks_words = ["شكر"  , "أشكرك", "ممتن" ,"تسلم"]
        return any(thank in token for thank in thanks_words)

    def isConfusionTool(self, token: str) -> bool:
        confusion = ["ماذا", "وضح", "اشرح"]
        return any(confused in token for confused in confusion)

    def isQuestion(self, tokens: list[str]) -> bool:
        if not len(tokens):
            return False
        if self.isQuestionTool(tokens[0]) or self.isQuestionTool(tokens[-1]) or self.isModalVerb(tokens[0]) :
            return True
        return False

    def isGoodbyeTool(self, token: str) -> bool:
        keywords = ["وداع", "باي","تمام","سلام"]
        return any(g in token for g in keywords)
