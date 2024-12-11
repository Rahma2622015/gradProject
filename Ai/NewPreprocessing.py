from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer


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

