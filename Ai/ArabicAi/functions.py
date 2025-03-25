class func:

    def isModalVerb(self, token: str) -> bool:
        return token in ["يكون", "يفعل", "لديه", "سوف", "يستطيع", "يمكن", "قد", "يجب", "ينبغي", "ربما", "قد يكون"]

    def isQuestionTool(self, token: str) -> bool:
        return token in ["ما", "ماذا", "أين", "متى", "من", "لمن", "أي", "لماذا", "كيف","هل"]

    def isGreetingTool(self, token: str) -> bool:
        greetings = [
            "اهلا", "مرحبا", "صباح الخير", "مساء الخير", "تحية طيبة", "سلام"
        ]
        return any(greet in token for greet in greetings)

    def isThanksTool(self, token: str) -> bool:
        thanks_words = [
            "شكرا", "أشكرك", "ممتن", "جزاك الله خيرا", "بارك الله فيك", "شكرًا جزيلاً", "كل الشكر"
        ]
        return any(thank in token for thank in thanks_words)

    def isConfusionTool(self, token: str) -> bool:
        confusion = ["ماذا", "لم أفهم", "وضح", "اشرح", "غير واضح", "أعد من فضلك"]
        return any(confused in token for confused in confusion)

    def isQuestion(self, tokens: list[str]) -> bool:
        if not len(tokens):
            return False
        if self.isQuestionTool(tokens[0]) or self.isQuestionTool(tokens[-1]) or self.isModalVerb(tokens[0]) :
            return True
        return False

    def isGoodbyeTool(self, token: str) -> bool:
        keywords = [
            "وَدَاع", "إلى اللقاء", "مع السلامة", "نراك لاحقًا", "في أمان الله",
            "حفظك الله", "نهارك سعيد", "يوم سعيد", "تصبح على خير", "أراك قريبًا"
        ]
        return any(g in token for g in keywords)
