import stanza
from Ai.ArabicAi.ArabicTokenizer import ArabicTokenizers
from Ai.ArabicAi.ArabicNormalizer import ArabicNormalize
import variables
A=ArabicNormalize()
import string

class ArabicPreprocessor:
    def __init__(self):
        self.nlp = stanza.Pipeline(lang="ar", processors="tokenize,lemma", download_method=None)

        with open(variables.NamesinCorrectArabic, "r", encoding="utf-8") as f:
            self.word = set(f.read().splitlines())

        with open(variables.CourseNameArabic, "r", encoding="utf-8") as f:
            self.course_name = set(f.read().splitlines())

    def lemmatization(self, sentences: list[list[str]]) -> list[list[str]]:
        lemmatized_sentences = []

        for sentence in sentences:
            sentence_text = " ".join(sentence)
            s = self.nlp(sentence_text)

            lemmas = []
            for sent in s.sentences:
                for word in sent.words:
                    original_word = word.text
                    if original_word in self.course_name or original_word in self.word:
                        lemmas.append(original_word)
                    else:
                        new_lemma = A.remove_diacritics(word.lemma)
                        lemmas.append(new_lemma)
            lemmatized_sentences.append(lemmas)

        return lemmatized_sentences

    def preprocess(self, sentences: list[list[str]]) -> list[list[str]]:
        return self.lemmatization(sentences)

    def is_course(self, word):
        word = word.lower()
        word_no_space = word.replace(" ", "")
        return word in self.course_name or word_no_space in self.course_name

    def extract_course_name(self, tokens: list[list[str]]) -> str | None:
        words = [token for sublist in tokens for token in sublist]
        potential_course_name = []

        for word in words:
            cleaned_word = word.strip(string.punctuation).lower()
            if self.is_course(cleaned_word):
                potential_course_name.append(cleaned_word)
            else:
                if potential_course_name:
                    return " ".join(potential_course_name)
                potential_course_name = []
        if potential_course_name:
            return " ".join(potential_course_name)

        return None

    def extract_all_course_names(self, tokens: list[list[str]]) -> list[str]:
        words = [token for sublist in tokens for token in sublist]  # Flatten
        course_names = []
        for word in words:
            cleaned_word = word.strip(string.punctuation).lower()
            if self.is_course(cleaned_word):
                course_names.append(cleaned_word)
        return list(set(course_names))

    def preprocess_text(self, tokens: list[list[str]]) -> str:
        words = [token for sublist in tokens for token in sublist]  # Flatten
        preprocessed_text = " ".join(words)
        return preprocessed_text


tt = ArabicTokenizers()
t = tt.tokenize("بيانات")
l = ArabicPreprocessor()
lemmas = l.preprocess(t)
print(lemmas)