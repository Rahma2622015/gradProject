from Database.FetchDataProfessors.findAssistant import FindAssistant

class CourseAssistant:
    def __init__(self):
        self.finder = FindAssistant()

    def get_courses_of_assistant(self, assistant_name):
        assistant, language = self.finder._find_assistant(assistant_name)

        if not assistant:
            return "No assistant found" if language == "en" else "لم يتم العثور على المعيد"

        name = assistant.name_arabic if language == "ar" else assistant.name
        prefix = "المعيد" if language == "ar" else "Assistant"

        if language == "ar":
            courses = [c.name_arabic for c in assistant.courses]
            no_courses = "لا توجد مواد"
        else:
            courses = [c.code for c in assistant.courses]
            no_courses = "No courses assigned"

        return f"{prefix} {name}: {', '.join(courses) if courses else no_courses}"
