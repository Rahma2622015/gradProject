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
    elif r[0] == ChatTask.CourseOfAssistant:
        return choice(data.get("CourseOfAssistant", [])).format(x=r[1], y=r[2])
    elif r[0] == ChatTask.CourseOfProfessor:
        return choice(data.get("CourseOfProfessor", [])).format(x=r[1], y=r[2])
    elif r[0] == ChatTask.DepartmentOfCourse:
        return choice(data.get("DepartmentOfCourse", [])).format(x=r[1], y=r[2])

    return None
