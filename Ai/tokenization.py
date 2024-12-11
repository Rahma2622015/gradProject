import nltk
class Tokenizer:
    def __init__(self):
        self.tokenizer = nltk.tokenize.PunktSentenceTokenizer()
    def SentenceTokenize(self, text:str)->list:
        sents = self.tokenizer.tokenize(text)
        return sents

    def WordTokenize(self,sents:list[str])->list[list[str]]:
        words=[nltk.word_tokenize(sentence) for sentence in sents]
        return words
    def tokenize(self,text:str)->list[list[str]]:
        return self.WordTokenize(self.SentenceTokenize(text))
