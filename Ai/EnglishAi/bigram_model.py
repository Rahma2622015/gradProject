from collections import defaultdict, Counter
import variables
from endPoints.ai_config_endpoints import load_ai_config


def config():
    return load_ai_config()


def use_smoothing_enabled():
    return config().get("use_smoothing", True)

class BigramModel:
    def __init__(self, bigrams_file=variables.Bigrams, names_file=variables.NamesinCorrectEnglish
                 ,courses_file=variables.courseLocation):
        self.bigrams = defaultdict(lambda: defaultdict(int))
        self.unigrams = Counter()
        self.total_bigrams = 0
        self.common_names = set()
        self.course_names = set()
        self.load_names(names_file)
        self.load_courses(courses_file)
        self.load_data(bigrams_file)


    def load_names(self, names_file):
        with open(names_file, 'r', encoding='utf-8') as f:
            for line in f:
                name = line.strip().lower()
                if name:
                    self.common_names.add(name)

    def load_courses(self, courses_file):
        with open(courses_file, 'r', encoding='utf-8') as f:
            for line in f:
                course = line.strip().lower()
                if course:
                    self.course_names.add(course)

    def _is_name(self, word):
        return word.lower() in self.common_names

    def _is_course(self, word):
        return word.lower() in self.course_names

    def preprocess_sentence(self, words):
        processed = []
        for w in words:
            lw = w.lower()
            if self._is_name(lw):
                processed.append("<Name>")
            elif self._is_course(lw):
                processed.append("<CourseName>")
            else:
                processed.append(lw)
        return processed
    def load_data(self, bigrams_file):
        with open(bigrams_file, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 3 and "Total Bigrams" not in line:
                    word1, word2, freq = parts
                    word1 = word1.lower()
                    word2 = word2.lower()
                    freq = int(freq)
                    self.bigrams[word1][word2] += freq
                    self.unigrams[word1] += freq
                    self.total_bigrams += freq

    def compute_bigrams(self, w1, w2):
        if w1 == "<Name>" or w2 == "<Name>":
            if w1 == "be" and w2 == "<Name>":
                return 0.8
            elif w1 == "<Name>" and w2 == "<end>":
                return 0.7

        w1 = w1.lower()
        w2 = w2.lower()
        bigram_freq = self.bigrams[w1].get(w2, 0)
        unigram_freq = self.unigrams.get(w1, 0)
        if use_smoothing_enabled():
         #print("i am using smoothing ...")
         return (bigram_freq + 1) / (unigram_freq + len(self.unigrams)) if unigram_freq > 0 else 0
        else:
            return  bigram_freq  / unigram_freq  if unigram_freq > 0 else 0

    def sentence_probability(self, sentences):
        results = []
        for words in sentences:
            processed_words = self.preprocess_sentence(words)
            words = ["<SOS>"] + processed_words + ["<END>"]

            probabilities = []
            for i in range(len(words) - 1):
                w1, w2 = words[i], words[i + 1]
                prob = self.compute_bigrams(w1, w2)
                probabilities.append(prob)

            avg_prob = sum(probabilities) / len(probabilities) if probabilities else 0
            unknown_ratio = sum(1 for p in probabilities if p == 0) / len(probabilities) if probabilities else 0

            print(f"\n Processed Sentence: {' '.join(words)}")
            print(" Bigram Probabilities:")
            for i in range(len(words) - 1):
                print(f"  - P({words[i + 1]} | {words[i]}) = {probabilities[i]:.6f}")
            #print(f" Unknown Ratio: {unknown_ratio:.2f}")
            #print(f" Average Probability: {avg_prob:.6f}")

            if unknown_ratio > 0.3:
                #print(" Result: UnknownTask (too many unknown bigrams)")
                results.append(("UnknownTask", probabilities, words))
            else:
                #print(" Result: Valid Sentence")
                results.append((avg_prob, probabilities, words))

        return results