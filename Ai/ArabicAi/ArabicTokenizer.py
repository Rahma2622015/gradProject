import re
import stanza
nlp = stanza.Pipeline(lang="ar", processors="tokenize,pos,lemma", download_method=None)
class ArabicTokenizers:
    def __init__(self):
        self.nlp = nlp
        self.pronouns = {"أنا", "أنت", "هو", "هي", "نحن", "أنتم", "أنهن", "هم", "هن"}

    def SentenceTokenize(self, text: str) -> list[str]:
            old_sentences = re.split(r"(?<=[.؟!])\s*", text)
            sentences = []
            for sentence in old_sentences:
                if sentence.strip():  # ‘عاوزة اتاكد انه الجملة مش فاضية عموما
                    sentences.append(sentence)
            return sentences

    def WordTokenize(self, sents: list[str]) -> list[list[str]]:
            tokenized_words = []
            for sent in sents:
                doc = self.nlp(sent)
                words = []
                for sentence in doc.sentences:
                    for word in sentence.words:
                        words.append(word.text)
                tokenized_words.append(words)

            return tokenized_words

    def tokenize(self, text: str) -> list[list[str]]:
            sents = self.SentenceTokenize(text)
            return self.WordTokenize(sents)

    def normalize(self, message: str) -> str:
        text = re.sub(r"\bانا\b", "أنا", message)
        return text

    def guess_pos(self, word: str, prev_word: str = None, prev_pos: str = None) -> str:
        if word in self.pronouns or word == "انا":
            return "PRON"
        #حروف عطف عندي فالعربي
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
                    words.append(word.text)
                    prev_word = words[j - 1] if j > 0 else None
                    prev_pos = tags[j - 1] if j > 0 else None
                    pos = word.upos if word.upos != "X" else self.guess_pos(word.text, prev_word, prev_pos)
                    tags.append(pos)

            pos_tags.append(tags)

        return pos_tags