from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

def isquestion(sentence):

    tokenized_sentence = word_tokenize(sentence)
    tagged_sentence = pos_tag(tokenized_sentence)

    if sentence.endswith('?') or any(word.lower() in ['what', 'when', 'where', 'why', 'how', 'who', 'which'] for word in tokenized_sentence):
        return True
    if  tagged_sentence[0][1] in ['VBZ', 'VBP', 'MD']:
        return True
    return False
sentence1 = "What is your name"
sentence2 = "This is a statement"
sentence3 = "Are you a chatbot?"
sentence4 = "You are a hagar."
sentence5="why"
