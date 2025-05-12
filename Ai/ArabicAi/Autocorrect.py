from spellchecker import SpellChecker
import variables

class ArabicSpellChecker:
    def __init__(self, dictionary_path = variables.arabic_word
                 ,names_path=variables.NamesInCorrectArabic
                 ,courses_path=variables.CourseNameArabic):
        self.spell = SpellChecker(language=None)
        self.spell.word_frequency.load_text_file(dictionary_path)

        with open(names_path, 'r', encoding='utf-8') as f:
          self.names_set = set(name.strip() for name in f if name.strip())
        with open(courses_path, 'r', encoding='utf-8') as f:
            course_names_set = set(course.strip() for course in f if course.strip())

        self.ignored_words = self.names_set.union(course_names_set)
    def auto_correct(self, sentence):
        words = sentence.split()
        corrected_words = []

        for word in words:
            if word in self.ignored_words:
                corrected_words.append(word)
            else:
                corrected_word = self.spell.correction(word)
                corrected_words.append(corrected_word if corrected_word else word)

        return " ".join(corrected_words)