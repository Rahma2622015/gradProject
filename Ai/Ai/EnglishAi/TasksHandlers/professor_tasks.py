from Ai.EnglishAi.chattask import ChatTask
from Database.Datastorage_DB import DatabaseStorage

def handle_professor_tasks(task, D: DatabaseStorage):
    responses = []

    person_name = None
    course_name = None
    dep_name = None
    role = None

    task_words = task[1] if isinstance(task, tuple) and len(task) > 1 else task
    pos_tags = task[2] if isinstance(task, tuple) and len(task) > 2 else []

    for i, tag in enumerate(pos_tags):
        if tag == "<CourseName>":
            course_name = task_words[i]
            print("course_name",course_name)
            role = "course"
            break

    if role is None:
        for i, word in enumerate(task_words):
            w = word.lower().strip()
            if w in ["professor", "dr.", "doctor", "dr", "assistant"]:
                remaining_words = task_words[i + 1:]
                person_name = " ".join(remaining_words)
                role = "professor"
                break

            elif w == "department":
                dep_name = " ".join(task_words[i + 1:])
                role = "department"
                break


    if task[0] == ChatTask.PersonRoleQueryTask:
        if role == "professor":
            description_of_prof = D.professors.get_professor_info(person_name)
            found = False
            if description_of_prof:
                found = True
                responses.append((ChatTask.ProfessorQueryTask, person_name, description_of_prof))
            else:
                description_of_ass = D.assistant.get_tasks_of_assistant(person_name)
                if description_of_ass:
                    found = True
                    responses.append((ChatTask.AssistantTask, person_name, description_of_ass))
            if not found:
                responses.append((ChatTask.UnknownTask, person_name, "there are no information about this person."))

        elif role == "department":
            head_name = D.head_department.get_head_of_department(dep_name)
            responses.append((ChatTask.HeadOfDepartment, dep_name, head_name))

    elif role == "course":
        professors = D.courseProfessor.get_professors_of_course(course_name)
        assistants = D.courseAssistant.get_assistants_of_course(course_name)

        if professors or assistants:
            combined_info = ""
            if professors:
                combined_info += " Professors:\n" + "\n".join(f"- {p}" for p in professors) + "\n\n"
            if assistants:
                combined_info += " Assistants:\n" + "\n".join(f"- {a}" for a in assistants)

            responses.append((ChatTask.ProfessorOfCourse, course_name, combined_info.strip()))
        else:
            responses.append((ChatTask.UnknownTask, "", "لم يتم التعرف على المطلوب."))
    else:
        responses.append((ChatTask.UnknownTask, "", ""))

    return responses
