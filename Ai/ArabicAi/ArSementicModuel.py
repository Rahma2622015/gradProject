from sklearn.metrics.pairwise import cosine_similarity
from Ai.ArabicAi.ArVectorizerModuel import SentenceVectorizer

class SentenceSimilarity:
    def __init__(self):
        self.vectorizer = SentenceVectorizer()
        self.threshold = 0.5

    def get_similarity(self, sentence1, sentence2):
        vec1 = self.vectorizer.to_vector(sentence1)
        vec2 = self.vectorizer.to_vector(sentence2)
        score = float(cosine_similarity([vec1], [vec2])[0][0])


        min_len = min(len(sentence1.split()), len(sentence2.split()))
        if min_len < 2 and score >= 0.5:
            score -= 0.5

        is_similar = score >= self.threshold
        return score, is_similar



