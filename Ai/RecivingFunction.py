from Data.dataStorage import DataStorage
from Ai import arabicFunction
from Ai import englishFunction

# def is_recommendation_task(tokens, pos, mapper, allowed_tasks=None) -> bool:
#     mapped_tasks = mapper.mapToken(tokens, pos)
#     if allowed_tasks is None:
#         allowed_tasks = [ChatTaskR.ExamSystem]
#     return any(task[0] in allowed_tasks for task in mapped_tasks)

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
        return arabicFunction.langArabic(message,storage)

    else:
        return "Sorry, I can't recognize this language.", None, None

