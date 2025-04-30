import stanza
from Ai.ArabicAi.ArabicTokenizer import ArabicTokenizers
from Ai.ArabicAi.ArabicNormalizer import ArabicNormalize
import variables

A=ArabicNormalize()
class ArabicPreprocessor:
    def __init__(self):
        self.nlp = stanza.Pipeline(lang="ar", processors="tokenize,lemma", download_method=None)

        with open(variables.NamesInCorrectArabic, "r", encoding="utf-8") as f:
            self.name = set(f.read().splitlines())

        with open(variables.CourseNameArabic, "r", encoding="utf-8") as f:
            self.course_name = set(f.read().splitlines())

        with open(variables.arabic_word, "r", encoding="utf-8") as f:
            self.word = set(f.read().splitlines())


    def lemmatization(self, sentences: list[list[str]]) -> list[list[str]]:
        lemmatized_sentences = []

        for sentence in sentences:
            sentence_text = " ".join(sentence)
            s = self.nlp(sentence_text)

            lemmas = []
            for sent in s.sentences:
                for word in sent.words:
                    original_word = word.text
                    if original_word in self.course_name or original_word in self.word or original_word in self.name:
                        lemmas.append(original_word)
                    else:
                        new_lemma = A.remove_diacritics(word.lemma)
                        lemmas.append(new_lemma)
            lemmatized_sentences.append(lemmas)

        return lemmatized_sentences

    def preprocess(self, sentences: list[list[str]]) -> list[list[str]]:
        return self.lemmatization(sentences)

tt=ArabicTokenizers()
t=tt.tokenize("بيانات")
l=ArabicPreprocessor()
lemmas=l.preprocess(t)
#print(lemmas)