from nltk import pos_tag
class PosTagging:

    def tag(self, sents: list[list[str]]) -> list[list[str]]:
        return [[tag[1] for tag in pos_tag(tokens)] for tokens in sents]

    #def ner(self, messages: list[list[str]]) -> list[list[tuple]]:
#     results = []
#     for message in messages:
#         text = " ".join(message)
#         doc = nlp(text)
#         entities = [(ent.text, ent.label_) for ent in doc.ents]
#         results.append(entities)
#     return results