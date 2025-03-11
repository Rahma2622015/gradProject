from autocorrect import Speller
class AutoCorrector:
    def __init__(self):
        self.spell = Speller()
    def correct_text(self, Message: str) -> str:
        return self.spell(Message)

