from Database.session import SessionLocal
from Database.DatabaseTabels.assistant import TeachingAssistant
from Database.utils import get_closest_match

class FindAssistant:
    def __init__(self):
        self.session = SessionLocal()

    def _find_assistant(self, name):
        def is_arabic(text):
            return any('\u0600' <= ch <= '\u06FF' for ch in text)

        language = "ar" if is_arabic(name) else "en"

        assistants = self.session.query(TeachingAssistant).filter(
            TeachingAssistant.name.ilike(f"%{name}%") |
            TeachingAssistant.name_arabic.ilike(f"%{name}%")
        ).all()

        if len(assistants) == 1:
            return assistants[0], language
        elif len(assistants) > 1:
            return assistants[0], language

        all_assistants = self.session.query(TeachingAssistant).all()
        names = [a.name for a in all_assistants if a.name] + \
                [a.name_arabic for a in all_assistants if a.name_arabic]

        matched = get_closest_match(name, names)
        if not matched:
            return None, language

        assistant = self.session.query(TeachingAssistant).filter(
            TeachingAssistant.name.ilike(f"%{matched}%") |
            TeachingAssistant.name_arabic.ilike(f"%{matched}%")
        ).first()

        return assistant, language if assistant else (None, language)
