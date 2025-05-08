from Database.FetchDataProfessors.findProfessor import FindProfessor

class ProfessorDescription:
    def __init__(self):
        self.find = FindProfessor()

    def get_professor_info(self, professor_name, language: str = "en"):
        professors = self.find._find_professor(professor_name)

        if not professors:
            return None

        title = "دكتور" if language == "ar" else "Professor"

        if len(professors) == 1:
            prof = professors[0]
            name = prof.name_arabic if language == "ar" else prof.name
            description = prof.description_arabic if language == "ar" else prof.description
            return f"{title} {name}: {description}"

        descriptions = []
        for prof in professors:
            name = prof.name_arabic if language == "ar" else prof.name
            desc = prof.description_arabic if language == "ar" else prof.description
            descriptions.append(f"{title} {name}: {desc}")

        if language == "ar":
            return "يوجد أكثر من دكتور بهذا الاسم، مثل:\n" + "\n".join(descriptions)
        else:
            return "There is more than one professor with this name, such as:\n" + "\n".join(descriptions)
