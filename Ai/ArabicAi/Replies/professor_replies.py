from Ai.ArabicAi.chattask import ChatTask
from random import choice

def handle_professor_reply(r, data):
    if r[0] == ChatTask.ProfessorQueryTask:
        professor_name = r[1] if len(r) > 1 and r[1] else "اسم الدكتور ليس متوفر"
        professor_info = r[2] if len(r) > 2 and r[2] else "لا يوجد معلومات كافية"
        return choice(data.get("ProfessorQueryTask", [])).format(x=professor_name, y=professor_info)
    elif r[0] == ChatTask.AssistantTask:
        return choice(data.get("AssistantTask", [])).format(x=r[1], y=r[2])
    elif r[0] == ChatTask.ProfessorOfCourse:
        return choice(data.get("ProfessorOfCourse", [])).format(x=r[1], y=r[2])
    elif r[0] == ChatTask.AssistantOfCourse:
        return choice(data.get("AssistantOfCourse", [])).format(x=r[1], y=r[2])
    elif r[0] == ChatTask.HeadOfDepartment:
        return choice(data.get("HeadOfDepartment", [])).format(x=r[1], y=r[2])
    else:
        return choice(data.get("Unknown", []))
