import stanza
class ArabicPreprocessor:
    def __init__(self):
        self.nlp = stanza.Pipeline(lang="ar", processors="tokenize,lemma", download_method=None)
    def lemmatization(self, sentences: list[list[str]]) -> list[list[str]]:
        lemmatized_sentences = []

        for sentence in sentences:
            sentence_text = " ".join(sentence)
            s = self.nlp(sentence_text)

            lemmas = []
            for sent in s.sentences:
                for word in sent.words:
                    lemmas.append(word.lemma)
            lemmatized_sentences.append(lemmas)
        return lemmatized_sentences

    def preprocess(self, sentences: list[list[str]]) -> list[list[str]]:
        return self.lemmatization(sentences)
