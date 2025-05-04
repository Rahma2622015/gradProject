from Ai.ArabicAi.chattask import ChatTask
from random import choice

def handle_course_reply(r, data):
    if r[0] == ChatTask.CourseQueryTask:
        return choice(data.get("CourseQueryTask", [])).format(x=r[1], y=r[2])
    elif r[0] == ChatTask.PrerequisiteQueryTask:
        return choice(data.get("PrerequisiteQueryTask", [])).format(x=r[1], y=r[2])
    elif r[0] == ChatTask.CourseHours:
        return choice(data.get("CourseHours", [])).format(x=r[1], y=r[2])
    elif r[0] == ChatTask.CourseDegrees:
        return choice(data.get("CourseDegrees", [])).format(x=r[1], y=r[2])
    elif r[0] == ChatTask.AssistantOfCourse:
        return choice(data.get("AssistantOfCourse", [])).format(x=r[1], y=r[2])
    elif r[0] == ChatTask.ProfessorOfCourse:
        return choice(data.get("ProfessorOfCourse", [])).format(x=r[1], y=r[2])
    elif r[0] == ChatTask.DepartmentOfCourse:
        return choice(data.get("DepartmentOfCourse", [])).format(x=r[1], y=r[2])
    else:
        return choice(data.get("Unknown", []))
