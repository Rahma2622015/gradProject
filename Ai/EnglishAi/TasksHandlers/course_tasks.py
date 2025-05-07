from Ai.EnglishAi.chattask import ChatTask
from Database.Datastorage_DB import DatabaseStorage

def handle_course_tasks(task, D: DatabaseStorage):
    description = D.courseDes
    hour = D.courseHour
    degree = D.courseDegree
    prerequisite = D.coursePre
    dep_of_course = D.courseDepartment
    ass_of_course = D.courseAssistant
    pro_of_course = D.courseProfessor

    responses = []
    person_name = None
    course_name = None
    role = None
    task_words = task[1] if isinstance(task, tuple) and len(task) > 1 else task
    pos_tags = task[2] if isinstance(task, tuple) and len(task) > 2 else []

    # Extract course name from POS tags
    for i, tag in enumerate(pos_tags):
        if tag == "<CourseName>":
            course_name = task_words[i]
            role = "course"
            break

    # Extract person name from POS tags
    for i, tag in enumerate(pos_tags):
        if tag == "<Name>":
            person_name = task_words[i]
            role = "professor"
            break

    # Detect role by keywords if not set yet
    lowered_words = [w.lower().strip() for w in task_words]
    for i, word in enumerate(lowered_words):
        if word in ["degree", "mark", "grade", "score"]:
            role = "degree"
            break
        elif word in ["hour", "hours", "credit"]:
            role = "hours"
            break
        elif word in ["prerequisite", "requirement", "require"]:
            role = "prerequisite"
            break
        elif word in ["department", "faculty", "college", "program"]:
            role = "program"
            break
    print("rr",role ," cname",course_name)
    if task[0] == ChatTask.CourseRoleQueryTask:
        try:
            if role == "degree" and course_name:
                val = degree.get_course_degree(course_name)
                responses.append((ChatTask.CourseDegrees, course_name, val))

            elif role == "hours" and course_name:
                val = hour.get_course_hours(course_name)
                responses.append((ChatTask.CourseHours, course_name, val))

            elif role == "prerequisite" and course_name:
                val = prerequisite.get_course_prerequisite(course_name)
                responses.append((ChatTask.PrerequisitesTask, course_name, val))

            elif role == "professor" and person_name:
                val_prof = pro_of_course.get_courses_of_professor(person_name)
                val_ass = ass_of_course.get_courses_of_assistant(person_name)
                found = False

                if val_prof:
                    found = True
                    responses.append((ChatTask.CourseOfProfessor, person_name, val_prof))

                if val_ass:
                    found = True
                    responses.append((ChatTask.CourseOfAssistant, person_name, val_ass))

                if not found:
                    responses.append((ChatTask.UnknownTask, person_name, "There is no information."))

            elif role == "program" and course_name:
                val = dep_of_course.get_department_of_course(course_name)
                responses.append((ChatTask.DepartmentOfCourse, course_name, val))

            elif role == "course" and course_name:
                val = description.get_course_description(course_name)
                responses.append((ChatTask.CourseQueryTask, course_name, val))

            else:
                responses.append((ChatTask.UnknownTask, course_name or person_name, "The question type could not be understood."))

        except Exception as e:
            responses.append((ChatTask.UnknownTask, course_name or person_name, f"An error occurred: {str(e)}"))

    else:
        responses.append((ChatTask.UnknownTask, "", "Unsupported task type."))

    return responses
