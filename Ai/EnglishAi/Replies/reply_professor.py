from random import choice
from Ai.EnglishAi.chattask import ChatTask

def handle_professor_tasks(r, data):
    if r[0] == ChatTask.ProfessorQueryTask:
        professor_name = r[1] if len(r) > 1 and r[1] else "Professor name not provided"
        professor_info = r[2] if len(r) > 2 and r[2] else "No Information Available"
        return choice(data.get("ProfessorQueryTask", [])).format(x=professor_name, y=professor_info)
    return None
