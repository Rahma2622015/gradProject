from sentence_transformers import SentenceTransformer

class SentenceVectorizer:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def to_vector(self, sentence):
        return self.model.encode(sentence, convert_to_numpy=True)