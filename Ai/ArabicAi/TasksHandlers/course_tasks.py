from Ai.ArabicAi.chattask import ChatTask
from Database.Datastorage_DB import DatabaseStorage


def handle_course_tasks(task, D: DatabaseStorage):
    responses = []
    course_name = ""
    keywords = ["مادة", "موضوع", "درس", "مقرر"]
    task_words = task[1] if isinstance(task, tuple) and len(task) > 1 else task

    for i, word in enumerate(task_words):
        if word in keywords:
            course_name = " ".join(task_words[i + 1:])
            print("🔍 Extracted cname:", course_name)
            break

    if course_name:
        if task[0] == ChatTask.CourseQueryTask:
            try:
                course_info = D.get_course_description_arabic(course_name)
                responses.append((ChatTask.CourseQueryTask, course_name, course_info))
            except Exception as e:
                responses.append((ChatTask.CourseQueryTask, course_name, "There was an error fetching the course description arabic."))

        elif task[0] == ChatTask.PrerequisiteQueryTask:
            try:
                course_info = D.get_course_prerequisite_arabic(course_name)
                responses.append((ChatTask.PrerequisiteQueryTask, course_name, course_info))
            except Exception as e:
                responses.append((ChatTask.PrerequisiteQueryTask, course_name, "There was an error fetching the prerequisites arabic."))

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
