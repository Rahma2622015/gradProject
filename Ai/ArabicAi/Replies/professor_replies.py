from Ai.ArabicAi.chattask import ChatTask
from random import choice

def handle_professor_reply(r, data):
    professor_name = r[1] if len(r) > 1 and r[1] else "اسم الدكتور ليس متوفر"
    professor_info = r[2] if len(r) > 2 and r[2] else "لا يوجد معلومات كافية"
    return choice(data.get("ProfessorQueryTask", [])).format(x=professor_name, y=professor_info)
