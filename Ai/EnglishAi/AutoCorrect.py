from autocorrect import Speller
import variables
class AutoCorrector:
    def __init__(self, names_file=variables.NamesinCorrectEnglish
                 ,course_file=variables.courseLocation):
        self.spell = Speller()
        self.names = self.load_names(names_file)
        self.course_names = self.load_names(course_file)

    def load_names(self, filename):
            with open(filename, "r", encoding="utf-8") as file:
                names = {line.strip().lower() for line in file}
            return names

    def correct_text(self, message: str) -> str:
        words = message.split()
        corrected_words = [
            word if word.lower() in self.names  or word.lower() in self.course_names
            else self.spell(word)
            for word in words
        ]
        return " ".join(corrected_words)