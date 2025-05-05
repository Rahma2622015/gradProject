from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from word2number import w2n


class Preprocessors:
    def __init__(self):
        self.lema = WordNetLemmatizer()

    def get_wordnet_pos(self, pos_tag: str) -> str:
        if pos_tag.startswith('NN'):
            return wordnet.NOUN
        elif pos_tag.startswith('VB'):
            return wordnet.VERB
        elif pos_tag.startswith('JJ'):
            return wordnet.ADJ
        else:
            return wordnet.NOUN

    def extract_first_number(self, data: list[list[str]], pos: list[list[str]]) -> int | None:
        for sentence_words, sentence_pos in zip(data, pos):
            for word, tag in zip(sentence_words, sentence_pos):
                if tag == 'CD':
                    word_lower = self.lowercase(word)
                    try:
                        return int(word_lower)
                    except ValueError:
                        try:
                            return w2n.word_to_num(word_lower)
                        except ValueError:
                            print(f"Warning: '{word}' is tagged as CD but not a recognizable number.")
                            continue
        return None

    def lowercase(self, text: str) -> str:
        return text.lower()

    def lemmatization(self, data: list[list[str]], pos: list[list[str]]) -> list[list[str]]:
        res = []
        print(pos)
        for i, x in enumerate(data):
            t = []
            for j, word in enumerate(x):
                t.append(self.lema.lemmatize(word, pos=self.get_wordnet_pos(pos[i][j])))
            res.append(t)

        return res

    def preprocess(self, data: list[list[str]], pos: list[list[str]]) -> list[list[str]]:
        return self.lemmatization(data, pos)

