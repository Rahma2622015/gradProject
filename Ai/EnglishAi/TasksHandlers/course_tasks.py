from Ai.EnglishAi.chattask import ChatTask
from Database.Datastorage_DB import DatabaseStorage


def handle_course_tasks(task, D: DatabaseStorage):
    responses = []
    course_name = ""
    task_words = task[1] if isinstance(task, tuple) and len(task) > 1 else task
    pos_tags = task[2] if isinstance(task, tuple) and len(task) > 2 else []
    print(task_words)
    print("p:", pos_tags)
    for i, tag in enumerate(pos_tags):
        if tag == "<CourseName>":
            course_name = task_words[i]
            print("🔍 Extracted cname from POS tag:", course_name)
            break

    if course_name:
        if task[0] == ChatTask.CourseQueryTask:
            try:
                course_info = D.get_course_description(course_name)
                responses.append((ChatTask.CourseQueryTask, course_name, course_info))
            except Exception as e:
                responses.append((ChatTask.CourseQueryTask, course_name, "There was an error fetching the course description ."))

        elif task[0] == ChatTask.PrerequisitesTask:
            try:
                course_info = D.get_course_prerequisite(course_name)
                responses.append((ChatTask.CourseQueryTask, course_name, course_info))
            except Exception as e:
                responses.append((ChatTask.CourseQueryTask, course_name, "There was an error fetching the prerequisites ."))

        elif task[0] == ChatTask.CourseHours:
            try:
                hours, degree = D.get_course_hours_and_degree(course_name)
                if not hours or not degree:
                    responses.append((ChatTask.CourseHours, course_name, "Course hours or degree not found in the database."))
                else:
                    responses.append((ChatTask.CourseHours, course_name, hours, degree))
            except Exception as e:
                responses.append((ChatTask.CourseHours, course_name, "There was an error fetching course hours or degree."))

    else:
        responses.append((ChatTask.CourseQueryTask, "Unknown", "Course name arabic could not be determined."))

    return responses
