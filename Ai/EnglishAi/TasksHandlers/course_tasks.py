from Ai.EnglishAi.chattask import ChatTask
from Database.Datastorage_DB import DatabaseStorage

def handle_course_tasks(task, D: DatabaseStorage):
    description = D.courseDes
    hour = D.courseHour
    degree = D.courseDegree
    prerequisite = D.coursePre
    dep_of_course = D.courseDepartment
    course_of_ass = D.courseAssistant
    course_of_prof = D.courseProfessor

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

    lowered_words = [w.lower().strip() for w in task_words]
    for i, word in enumerate(lowered_words):
        if word in ["degree", "mark", "grade", "score"]:
            role = "degree"
            break
        elif word in ["professor", "dr.", "dr", "doctor"]:
            role = "professor"
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
        elif word in ["course", "subject", "lesson"]:
            next_words = task_words[i + 1:]  # قائمة من الكلمات بعد "مادة"
            found_doctor = False
            for j, w in enumerate(next_words):
                if w in ["professor", "dr.", "dr", "doctor"]:
                    person_name = " ".join(next_words[j + 1:])
                    role = "professor"
                    found_doctor = True
                    break
            if not found_doctor:
                course_name = " ".join(next_words)
                role = "course"
            break
    print("role ",role," course_name ",course_name," person_name ",person_name)
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
                if val:
                    responses.append((ChatTask.PrerequisitesTask, course_name, val))
                else:
                    responses.append((ChatTask.PrerequisitesTask, course_name, "There are no prerequisites of this course."))

            elif role == "professor" and person_name:
                val_prof = course_of_prof.get_courses_of_professor(person_name)
                found = False
                if val_prof:
                    found = True
                    responses.append((ChatTask.CourseOfProfessor, val_prof))
                else:
                    val_ass = course_of_ass.get_courses_of_assistant(person_name)
                    if val_ass:
                        found = True
                        responses.append((ChatTask.CourseOfAssistant, val_ass))
                if not found:
                    responses.append((ChatTask.UnknownTask, person_name, "There is no information."))

            elif role == "program" and course_name:
                val = dep_of_course.get_department_of_course(course_name)
                responses.append((ChatTask.DepartmentOfCourse, course_name, val))

            elif role == "course" and course_name:
                val = description.get_course_description(course_name)
                responses.append((ChatTask.CourseQueryTask, val))

            else:
                responses.append((ChatTask.UnknownTask, course_name or person_name, "The question type could not be understood."))

        except Exception as e:
            responses.append((ChatTask.UnknownTask, course_name or person_name, f"An error occurred: {str(e)}"))

    else:
        responses.append((ChatTask.UnknownTask, "", "Unsupported task type."))

    return responses