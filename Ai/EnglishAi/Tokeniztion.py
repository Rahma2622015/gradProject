from flair.data import Sentence
from flair.splitter import SegtokSentenceSplitter
from flair.models import SequenceTagger

class Tokenizers:
    def __init__(self):
        self.sentence_splitter = SegtokSentenceSplitter()
        self.pos_tagger = SequenceTagger.load("pos")

    def SentenceTokenize(self, text: str) -> list[str]:
        sentences = self.sentence_splitter.split(text)
        return [sentence.to_plain_string() for sentence in sentences]

    def WordTokenize(self, sents: list[str]) -> list[list[str]]:
        tokenized_words = []

        for sentence in sents:
            flair_sentence = Sentence(sentence)
            words = [token.text for token in flair_sentence.tokens]
            tokenized_words.append(words)

        return tokenized_words

    def tokenize(self, message: str) -> list[list[str]]:
        sents = self.SentenceTokenize(message)
        return self.WordTokenize(sents)

    def pos_tag(self, sents: list[list[str]]) -> list[list[str]]:
        pos_tags = []

        for sentence in sents:
            flair_sentence = Sentence(' '.join(sentence))
            print(flair_sentence)
            self.pos_tagger.predict(flair_sentence)
            tags = [token.labels[0].value for token in flair_sentence.tokens]

            pos_tags.append(tags)

        return pos_tags