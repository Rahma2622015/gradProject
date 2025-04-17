from flair.data import Sentence
from flair.splitter import SegtokSentenceSplitter
from flair.models import SequenceTagger
import re
import string

def load_course_names(file_path=r"F:\gradProject\Ai\EnglishAi\courses.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            courses = {line.strip().lower() for line in file if line.strip()}
        return courses
    except FileNotFoundError:
        return {"skill 401", "comp301", "math 101", "comp 202", "religion and safety"}

COURSE_NAMES = load_course_names()

class Tokenizers:
    def __init__(self):
        self.sentence_splitter = SegtokSentenceSplitter()
        self.pos_tagger = SequenceTagger.load("pos")
        self.course_pattern = re.compile(r'([a-zA-Z]+)\s+(\d{3})')
        self.phrases_pattern = re.compile(
            '|'.join(
                re.escape(phrase.lower())
                for phrase in sorted(COURSE_NAMES, key=len, reverse=True)
                if ' ' in phrase
            ),
            re.IGNORECASE
        )

    def preprocess_phrases(self, text):
        def replacer(match):
            return match.group(0).replace(' ', '')

        return self.phrases_pattern.sub(replacer, text)

    def preprocess_text(self, text):
        text = self.preprocess_phrases(text)
        matches = list(self.course_pattern.finditer(text))
        if matches:
            for match in reversed(matches):
                start, end = match.span()
                course_name = match.group(1) + match.group(2)
                text = text[:start] + course_name + text[end:]
        return text

    def SentenceTokenize(self, text: str) -> list[str]:
        text = self.preprocess_text(text)
        sentences = self.sentence_splitter.split(text)
        return [sentence.to_plain_string() for sentence in sentences]

    def tokenize(self, text: str) -> list[list[str]]:
        text = self.preprocess_text(text)
        sentences = self.sentence_splitter.split(text)
        tokenized_words = []

        for sentence in sentences:
            flair_sentence = Sentence(sentence.to_plain_string())
            words = [token.text for token in flair_sentence.tokens]
            tokenized_words.append(words)

        return tokenized_words

    def is_course(self, word):
        word = word.lower()
        word_no_space = word.replace(" ", "")
        return word in COURSE_NAMES or word_no_space in COURSE_NAMES

    def extract_course_name(self, text: str) -> str | None:
        preprocessed_text = self.preprocess_text(text)
        words = preprocessed_text.split()

        for word in words:
            cleaned_word = word.strip(string.punctuation).lower()
            if self.is_course(cleaned_word):
                return cleaned_word

        return None

    def extract_all_course_names(self, text: str) -> list[str]:
        preprocessed_text = self.preprocess_text(text)
        words = preprocessed_text.split()
        course_names = []

        for word in words:
            cleaned = word.strip(string.punctuation).lower()
            if self.is_course(cleaned):
                course_names.append(cleaned)

        return list(set(course_names))

    def pos_tag(self, sents: list[list[str]]) -> list[list[str]]:
        pos_tags = []

        for sentence in sents:
            flair_sentence = Sentence(' '.join(sentence))
            self.pos_tagger.predict(flair_sentence)

            tags = []
            for token in flair_sentence.tokens:
                word = token.text
                if self.is_course(word):
                    tags.append("<CourseName>")
                else:
                    tags.append(token.labels[0].value)

            pos_tags.append(tags)

        print(pos_tags)
        return pos_tags