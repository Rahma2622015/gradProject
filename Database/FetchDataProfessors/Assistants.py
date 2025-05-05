from Database.session import SessionLocal
from Database.DatabaseTabels.assistant import TeachingAssistant

class Assistant:
    def __init__(self):
        self.session = SessionLocal()

    def get_tasks_of_assistant(self,assistant_name, language: str = "en"):
        assistant = self.session.query(TeachingAssistant).filter(
            TeachingAssistant.name.ilike(f"%{assistant_name}%")|
            TeachingAssistant.name_arabic.ilike(f"%{assistant_name}%")
        ).first()
        if assistant:
            if language=="ar":
                return assistant.description_arabic
            return assistant.description
        return None
