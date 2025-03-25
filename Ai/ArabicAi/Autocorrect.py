from spellchecker import SpellChecker

class ArabicSpellChecker:
    def __init__(self, dictionary_path):
        self.spell = SpellChecker(language=None)
        self.spell.word_frequency.load_text_file(dictionary_path)

    def auto_correct(self, sentence):
        words = sentence.split()
        corrected_words = []

        for word in words:
            corrected_word = self.spell.correction(word)
            if corrected_word:
                corrected_words.append(corrected_word)
            else:
                corrected_words.append(word)

        return " ".join(corrected_words)
