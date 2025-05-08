from random import choice
from Ai.EnglishAi.chattask import ChatTask

def handle_professor_tasks(r, data):
    if r[0] == ChatTask.ProfessorQueryTask:
        professor_info =r[1] if len(r) > 1 and r[1] else "No Information Available"
        return choice(data.get("ProfessorQueryTask", [])).format(x=professor_info)
    elif r[0] == ChatTask.AssistantTask:
        return choice(data.get("AssistantTask", [])).format(x=r[1])
    elif r[0] == ChatTask.ProfessorOfCourse:
        return choice(data.get("ProfessorOfCourse", [])).format(x=r[1], y=r[2])
    elif r[0] == ChatTask.HeadOfDepartment:
        return choice(data.get("HeadOfDepartment", [])).format(x=r[1], y=r[2])

    return None
