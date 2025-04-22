from sklearn.metrics.pairwise import cosine_similarity
from Ai.EnglishAi.VectorizerModule import SentenceVectorizer

class SentenceSimilarity:
    def __init__(self):
        self.vectorizer = SentenceVectorizer()
        self.threshold = 0.5

    def get_similarity(self, sentence1, sentence2):
        vec1 = self.vectorizer.to_vector(sentence1)
        vec2 = self.vectorizer.to_vector(sentence2)
        score=  float(cosine_similarity([vec1], [vec2])[0][0])
        is_similar = score >= self.threshold
        return score, is_similar
