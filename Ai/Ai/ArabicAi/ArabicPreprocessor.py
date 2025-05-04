import stanza
from Ai.ArabicAi.ArabicTokenizer import ArabicTokenizers
from Ai.ArabicAi.ArabicNormalizer import ArabicNormalize
import variables

A=ArabicNormalize()
import string

class ArabicPreprocessor:
    def __init__(self):
        self.nlp = stanza.Pipeline(lang="ar", processors="tokenize,lemma", download_method=None)

        with open(variables.NamesInCorrectArabic, "r", encoding="utf-8") as f:
            self.name = set(f.read().splitlines())

        with open(variables.CourseNameArabic, "r", encoding="utf-8") as f:
            self.course_name = set(f.read().splitlines())

        with open(variables.arabic_word, "r", encoding="utf-8") as f:
            self.word = set(f.read().splitlines())


    def lemmatization(self, sentences: list[list[str]]) -> list[list[str]]:
        lemmatized_sentences = []

        for sentence in sentences:
            sentence_text = " ".join(sentence)
            s = self.nlp(sentence_text)

            lemmas = []
            for sent in s.sentences:
                for word in sent.words:
                    original_word = word.text
                    if original_word in self.course_name or original_word in self.word or original_word in self.name:
                        lemmas.append(original_word)
                    else:
                        new_lemma = A.remove_diacritics(word.lemma)
                        lemmas.append(new_lemma)
            lemmatized_sentences.append(lemmas)

        return lemmatized_sentences

    def preprocess(self, sentences: list[list[str]]) -> list[list[str]]:
        return self.lemmatization(sentences)


    def is_course(self, word):
        word = word.lower()
        word_no_space = word.replace(" ", "")
        return word in self.course_name or word_no_space in self.course_name

    def extract_course_name(self, tokens: list[list[str]]) -> str | None:
        words = [token for sublist in tokens for token in sublist]
        potential_course_name = []

        for word in words:
            cleaned_word = word.strip(string.punctuation).lower()
            if self.is_course(cleaned_word):
                potential_course_name.append(cleaned_word)
            else:
                if potential_course_name:
                    return " ".join(potential_course_name)
                potential_course_name = []
        if potential_course_name:
            return " ".join(potential_course_name)

        return None

    def extract_all_course_names(self, text: str) -> list[str]:
        sentences = text.split(".")
        tokenized_sentences = [sentence.strip().split() for sentence in sentences if sentence.strip()]

        preprocessed_text = self.preprocess_text(tokenized_sentences)
        words = preprocessed_text.split()
        course_names = []

        for word in words:
            cleaned = word.strip(string.punctuation).lower()
            if self.is_course(cleaned):
                course_names.append(cleaned)

        return list(set(course_names))

    def extract_first_number_ar(self, data: list[list[str]], pos: list[list[str]]) -> int | None:
        word_to_num = {
            'واحد': 1, 'اثنين': 2, 'اثنان': 2, 'ثلاثة': 3, 'أربعة': 4, 'خمسة': 5,
            'ستة': 6, 'سبعة': 7, 'ثمانية': 8, 'تسعة': 9, 'عشرة': 10,
            'أحد عشر': 11, 'اثنا عشر': 12, 'ثلاثة عشر': 13, 'أربعة عشر': 14,
            'خمسة عشر': 15, 'ستة عشر': 16, 'سبعة عشر': 17, 'ثمانية عشر': 18,
            'تسعة عشر': 19, 'عشرون': 20
        }

        for sentence_words, sentence_pos in zip(data, pos):
            for word, tag in zip(sentence_words, sentence_pos):
                if tag == 'NUM':
                    word = word.strip().lower()
                    # تحويل الأرقام العربية إلى أرقام إنجليزية
                    word = word.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))
                    try:
                        return int(word)
                    except ValueError:
                        if word in word_to_num:
                            return word_to_num[word]
                        else:
                            print(f"Warning: '{word}' is tagged as NUM but not a recognizable number.")
                            continue
        return None

    def preprocess_text(self, tokens: list[list[str]]) -> str:
        words = [token for sublist in tokens for token in sublist]  # Flatten
        preprocessed_text = " ".join(words)
        return preprocessed_text



