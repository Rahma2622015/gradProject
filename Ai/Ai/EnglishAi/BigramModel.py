from collections import defaultdict, Counter
class BigramModel:
    def __init__(self, bigram_file):
        self.bigrams = defaultdict(lambda: defaultdict(int))
        self.unigrams = Counter()
        self.total_bigrams = 0
        self.load_data(bigram_file)

    def load_data(self, bigram_file):
        with open(bigram_file, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 3:
                    word1, word2, freq = parts
                    freq = int(freq)
                    self.bigrams[word1][word2] += freq
                    self.unigrams[word1] += freq
                    self.total_bigrams += freq
                    #print(f"Loaded Bigram: {word1} {word2} with frequency {freq}")

    def compute_bigrams(self, w1, w2):
        bigram_freq = self.bigrams[w1].get(w2, 0)
        unigram_freq = self.unigrams.get(w1, 0)
        return bigram_freq / unigram_freq if unigram_freq > 0 else 0

    def sentence_probability(self, sentences):
        results = []

        for words in sentences:
            words = ["<SOS>"] + words + ["<END>"]
            probabilities = [self.compute_bigrams(words[i], words[i + 1]) for i in range(len(words) - 1)]
            avg_prob = sum(probabilities) / len(probabilities) if probabilities else 0

            print(f"\nProcessed Sentence: {' '.join(words)}")
            print(f"Total Probability: {avg_prob:.6f}\n")
            print("Bigram Probabilities:")
            for i in range(len(words) - 1):
                w1, w2 = words[i], words[i + 1]
                prob = self.compute_bigrams(w1, w2)
                print(f"  - P({w2} | {w1}) = {prob:.6f}")

            if all(p == 0 for p in probabilities):
                print("=> Result: UnknownTask (all bigrams are zero)")
                results.append(("UnknownTask", probabilities, words))
            else:
                results.append((avg_prob, probabilities, words))
        return results

