import stanza

class ArabicGrammarChecker:
    def __init__(self):
        self.nlp = stanza.Pipeline(lang='ar', processors='tokenize,pos',download_method=None)

    def is_correct(self, lemmatized_sentences: list[list[str]]) -> list[bool]:
        results = []
        for tokens in lemmatized_sentences:
            sentence = ' '.join(tokens)
            doc = self.nlp(sentence)
            has_error = self.has_agreement_error(doc)
            results.append(not has_error)
        return results

    def get_errors(self, lemmatized_sentences: list[list[str]]) -> list[list[str]]:
        all_errors = []
        for tokens in lemmatized_sentences:
            sentence = ' '.join(tokens)
            doc = self.nlp(sentence)
            errors = self.extract_agreement_errors(doc)
            all_errors.append(errors)
        return all_errors

    def has_agreement_error(self, doc) -> bool:
        for sentence in doc.sentences:
            for i in range(len(sentence.words) - 1):
                w1 = sentence.words[i]
                w2 = sentence.words[i + 1]
                if w1.upos in ['NOUN', 'ADJ'] and w2.upos in ['ADJ', 'NOUN']:
                    if w1.feats and w2.feats:
                        if not self.feats_agree(w1.feats, w2.feats):
                            return True
        return False

    def extract_agreement_errors(self, doc) -> list[str]:
        errors = []
        for sentence in doc.sentences:
            for i in range(len(sentence.words) - 1):
                w1 = sentence.words[i]
                w2 = sentence.words[i + 1]
                if w1.upos in ['NOUN', 'ADJ'] and w2.upos in ['ADJ', 'NOUN']:
                    if w1.feats and w2.feats:
                        if not self.feats_agree(w1.feats, w2.feats):
                            errors.append(f"عدم تطابق '{w1.text}' و '{w2.text}'")
        return errors

    def feats_agree(self, feats1: str, feats2: str) -> bool:
        f1 = {kv.split('=')[0]: kv.split('=')[1] for kv in feats1.split('|') if '=' in kv}
        f2 = {kv.split('=')[0]: kv.split('=')[1] for kv in feats2.split('|') if '=' in kv}
        for key in ['Gender', 'Number']:
            if key in f1 and key in f2 and f1[key] != f2[key]:
                return False
        return True