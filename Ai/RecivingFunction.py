from Modules.dataStorage import DataStorage
from Ai.ArabicReceving import arabicFunction
from Ai.EnglishReceving import englishFunction

import re

def detect_language(text):
    if re.search(r'[\u0600-\u06FF]', text):
        return "Arabic"
    elif re.search(r'[A-Za-z]', text):
        return "English"
    else:
        return "Unknown"


def receive(message: str, storage: DataStorage):

    languag = detect_language(message)

    if languag == "English":
       return  englishFunction.langEnglish(message, storage)

    elif languag == "Arabic":
        return arabicFunction.langArabic(message, storage)

    else:
        return "Sorry, I can't recognize this language.", None, None

