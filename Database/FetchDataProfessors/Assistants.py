from Database.FetchDataProfessors.findAssistant import FindAssistant  # غيّري المسار حسب المشروع

class Assistant:
    def __init__(self):
        self.finder = FindAssistant()

    def get_tasks_of_assistant(self, assistant_name):
        assistant, language = self.finder._find_assistant(assistant_name)

        prefix = "المعيد" if language == "ar" else "Assistant"

        if not assistant:
            return "لم يتم العثور على المعيد" if language == "ar" else "Assistant not found"

        name = assistant.name_arabic if language == "ar" else assistant.name
        desc = assistant.description_arabic if language == "ar" else assistant.description

        return f"{prefix} {name}: {desc if desc else ('لا يوجد وصف' if language == 'ar' else 'No description')}"
