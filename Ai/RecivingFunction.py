from Data.dataStorage import DataStorage
from Ai import arabicFunction
from Ai import englishFunction

import re

def detect_language(text):
    if re.search(r'[\u0600-\u06FF]', text):
        return "Arabic"
    elif re.search(r'[A-Za-z]', text):
        return "English"
    else:
        return "Unknown"


def receive(message: str, storage: DataStorage, user_id: str):

    languag = detect_language(message)

    if languag == "English":
       return  englishFunction.langEnglish(message,storage,user_id)

    elif languag == "Arabic":
        return arabicFunction.langArabic(message,storage,user_id)

    else:
        return "Sorry, I can't recognize this language.", None, None

