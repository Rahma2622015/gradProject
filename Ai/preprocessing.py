from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet


class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.lema = WordNetLemmatizer()

    def get_wordnet_pos(self, tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('P'):
            return wordnet.NOUN
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    def lowercase(self, text:str)->str:
        return text.lower()

    def remove_punctuation(self, text:str)->str:
        return ''.join(char for char in text if char.isalpha() or char == ' ')

    #def remove_stop_words(self, sentences: list[list[str]]) -> list[list[str]]:
    #    return [[token for token in sentence if token not in self.stop_words] for sentence in sentences]

    # def stem(self, sentences: list[list[str]],pos:list[list[str]]) -> list[list[str]]:
    #     return [[self.stemmer.stem(token) for token in sentence] for sentence in sentences]

    def lemmatization(self, data: list[list[str]], pos: list[list[str]]) -> list[list[str]]:
        res = []
        #print(pos)
        for i, x in enumerate(data):
            t = []
            for j, word in enumerate(x):
                t.append(self.lema.lemmatize(word, pos=self.get_wordnet_pos(pos[i][j])))
            res.append(t)

        return res

    def preprocess(self, data: list[list[str]], pos: list[list[str]]) -> list[list[str]]:
        return self.lemmatization(data, pos)

