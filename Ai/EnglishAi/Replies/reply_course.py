from random import choice
from Ai.EnglishAi.chattask import ChatTask

def handle_course_tasks(r, data):
    if r[0] == ChatTask.CourseQueryTask:
        return choice(data.get("CourseQueryTask", [])).format(x=r[1], y=r[2])
    elif r[0] == ChatTask.CourseHours:
        return choice(data.get("CourseHours", [])).format(x=r[1], y=r[2], z=r[3])
    elif r[0] == ChatTask.PrerequisitesTask:
        if isinstance(r[2], str):
            return r[2]
        else:
            prereq_list = r[2]
            prereq_names = prereq_list[0] if len(prereq_list) == 1 else ", ".join(prereq_list)
            return choice(data.get("PrerequisitesTask", [])).format(x=prereq_names, y=r[1])
    return None
