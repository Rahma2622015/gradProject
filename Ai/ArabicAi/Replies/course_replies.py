from Ai.ArabicAi.chattask import ChatTask
from random import choice

def handle_course_reply(r, data):
    if r[0] == ChatTask.CourseQueryTask:
        return choice(data.get("CourseQueryTask", [])).format(x=r[1], y=r[2])
    elif r[0] == ChatTask.PrerequisiteQueryTask:
        return choice(data.get("PrerequisiteQueryTask", [])).format(x=r[1], y=r[2])
    elif r[0] == ChatTask.CourseHours:
        return choice(data.get("CourseHours", [])).format(x=r[1], y=r[2], z=r[3])
    else:
        return choice(data.get("Unknown", []))
