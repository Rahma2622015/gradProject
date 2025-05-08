import re
import stanza
import variables
from  Ai.ArabicAi.ArabicNormalizer import ArabicNormalize
nlp = stanza.Pipeline(lang="ar", processors="tokenize,pos,lemma", download_method=None)
normalizer=ArabicNormalize()
class ArabicTokenizers:
    def __init__(self):
        self.nlp = nlp
        self.pronouns = {"أنا", "أنت", "هو", "هي", "نحن", "أنتم", "أنهن", "هم", "هن"}
        with open(variables.NamesInCorrectArabic, "r", encoding="utf-8") as f:
            self.known_names = set(f.read().splitlines())
        with open(variables.CourseNameArabic, "r", encoding="utf-8") as f:
            self.course_names = sorted(f.read().splitlines(), key=len, reverse=True)
            # تحميل الكلمات الممنوعة من التقسيم (من ملف arabic_words.txt)
        with open(variables.arabic_word, "r", encoding="utf-8") as f:
            self.no_split_words = set(f.read().splitlines())

    def SentenceTokenize(self, text: str) -> list[str]:
        old_sentences = re.split(r"(?<=[.؟!])\s*", text)
        sentences = [sentence for sentence in old_sentences if sentence.strip()]
        return sentences

    def WordTokenize(self, sents: list[str]) -> list[list[str]]:
        tokenized_words = []
        for sent in sents:
            doc = self.nlp(sent)
            words = []
            for sentence in doc.sentences:
                for word in sentence.words:
                    # إذا كانت الكلمة في قائمة الكلمات الممنوعة من التقسيم
                    if word.text in self.no_split_words:
                        words.append(word.text)
                    else:
                        words.append(word.text)
            tokenized_words.append(words)

        return tokenized_words

    def tokenize(self, text: str) -> list[list[str]]:
        normalized_text = self.normalize(text)
        sents = self.SentenceTokenize(normalized_text)
        return self.WordTokenize(sents)

    def normalize(self, message: str) -> str:
        return normalizer.normalize(message)
    def guess_pos(self, word: str, prev_word: str = None, prev_pos: str = None) -> str:
        if word in self.pronouns or word == "أنا":
            return "PRON"
        elif word.startswith("و") or word.startswith("ف"):
            return "CCONJ"
        elif word.startswith("ال"):
            return "NOUN"
        elif word.startswith("سوف"):
            return "VERB"
        elif re.search(r"\b(أن|لن|لم)\b", word):
            return "VERB"
        elif prev_word in self.pronouns or prev_pos == "PRON":
            return "NOUN"
        else:
            return "NOUN"

    def pos_tag(self, tokenized_sents: list[list[str]]) -> list[list[str]]:
        pos_tags = []
        for sentence in tokenized_sents:
            sent_text = " ".join(sentence)
            sent_text = self.normalize(sent_text)
            s = self.nlp(sent_text)

            tags = []
            words = []

            for i, sent in enumerate(s.sentences):
                for j, word in enumerate(sent.words):
                    original_word = word.text
                    words.append(original_word)

                    prev_word = words[j - 1] if j > 0 else None
                    prev_pos = tags[j - 1] if j > 0 else None

                    if original_word in self.known_names:
                        pos = "<NAME>"
                    elif original_word in self.course_names:
                        pos = "<CourseName>"
                    else:
                        pos = word.upos if word.upos != "X" else self.guess_pos(original_word, prev_word, prev_pos)

                    tags.append(pos)

            pos_tags.append(tags)
        return pos_tags