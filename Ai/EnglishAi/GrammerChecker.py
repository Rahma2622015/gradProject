import re

import language_tool_python

class EnglishGrammarChecker:
    def __init__(self):
        self.tool = language_tool_python.LanguageTool('en-US')

    def fix_pronoun_i(self, sentence: str) -> str:
        return re.sub(r'\bi\b', 'I', sentence)

    def is_correct(self, lemmatized_sentences: list[list[str]]) -> list[bool]:
        results = []
        for sentence_tokens in lemmatized_sentences:
            sentence = ' '.join(sentence_tokens)
            if sentence:
                sentence = sentence[0].upper() + sentence[1:]
                sentence = self.fix_pronoun_i(sentence)
            matches = self.tool.check(sentence)
            grammar_matches = [m for m in matches if "spelling mistake" not in m.message.lower()]
            results.append(len(grammar_matches) == 0)
        return results

    def get_errors(self, lemmatized_sentences: list[list[str]]) -> list[list[str]]:
        all_errors = []
        for sentence_tokens in lemmatized_sentences:
            sentence = ' '.join(sentence_tokens)
            if sentence:
                sentence = sentence[0].upper() + sentence[1:]
            matches = self.tool.check(sentence)
            errors = [match.message for match in matches]
            all_errors.append(errors)
        return all_errors
