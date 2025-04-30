from Ai.EnglishAi.chattask import ChatTask
from Database.Datastorage_DB import DatabaseStorage

def handle_professor_tasks(task, D: DatabaseStorage):
    responses = []

    if task[0] == ChatTask.ProfessorQueryTask:
        professor_name = None
        keywords = ["professor", "dr.", "doctor","dr"]
        task_words = task[1] if isinstance(task, tuple) and len(task) > 1 else task
        for i, word in enumerate(task_words):
            if word.lower().strip() in keywords and i + 1 < len(task_words):
                professor_name = " ".join(task_words[i + 1:])
                print("🔍 Extracted name:", professor_name)
                break
        if professor_name:
            professor_info = D.get_professor_info(str(professor_name))
        else:
            professor_name = "Unknown"
            professor_info = "No information available"

        responses.append((ChatTask.ProfessorQueryTask, professor_name, professor_info))

    return responses
