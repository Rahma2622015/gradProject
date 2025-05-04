from Ai.EnglishAi.chattask import ChatTask
from Database.Datastorage_DB import DatabaseStorage

def handle_professor_tasks(task, D: DatabaseStorage):
    responses = []

    person_name = None
    course_name = None
    dep_name = None
    role=None
    task_words = task[1] if isinstance(task, tuple) and len(task) > 1 else task

    # تحديد نوع السؤال (دكتور، معيد، رئيس قسم...)
    for i, word in enumerate(task_words):
        w = word.lower().strip()

        if w in ["دكتور", "د.", "أستاذ", "د", "مدرس"]:
            remaining_words = task_words[i + 1:]
            role_found = False
            for j, next_word in enumerate(remaining_words):
                nw = next_word.lower()
                if nw in ["مادة", "درس", "موضوع"]:
                    if j + 1 < len(remaining_words):
                        course_name = " ".join(remaining_words[j + 1:])
                        print(course_name, "<--- course_name")
                        role = "مادة"
                        role_found = True
                        break
            if not role_found:
                person_name = " ".join(remaining_words)
                print(person_name, "<--- person_name")
                role = "دكتور"
            break

        elif w in ["قسم"]:
            dep_name = " ".join(task_words[i + 1:])
            role = "قسم"
            break
        else:
            continue

    # التعامل مع كل حالة بناءً على الدور المستخرج
    if task[0] == ChatTask.PersonRoleQueryTask:
        if role == "دكتور":
            description_of_prof = D.professors.get_professor_info(person_name,"ar")
            description_of_ass = D.assistant.get_tasks_of_assistant(person_name,"ar")

            found = False

            if  description_of_prof:
                found = True
                responses.append((ChatTask.ProfessorQueryTask, person_name, description_of_prof))

            if  description_of_ass:
                found = True
                responses.append((ChatTask.AssistantTask, person_name, description_of_ass))

            if not found:
                responses.append(
                    (ChatTask.UnknownTask, person_name, "لا يوجد معلومات عن هذا الشخص لا كدكتور ولا كمعيد."))


        elif role == "قسم":
            head_name = D.head_department.get_head_of_department(dep_name,"ar")
            responses.append((ChatTask.HeadOfDepartment, dep_name, head_name))

        elif role == "مادة":
            # ممكن السؤال يكون "مين الدكتور اللي بيدرس مادة كذا؟"
            professors = D.courseProfessor.get_professors_of_course(course_name,"ar")
            if professors:
                responses.append((ChatTask.ProfessorOfCourse, course_name, professors))
            else:
                assistants = D.courseAssistant.get_assistants_of_course(course_name, "ar")
                if assistants:
                    responses.append((ChatTask.AssistantOfCourse, course_name, assistants))
                else:
                    responses.append((ChatTask.UnknownTask, "", "لم يتم التعرف على المطلوب."))
        else:
            responses.append((ChatTask.UnknownTask, "", "لم يتم التعرف على المطلوب."))
    else:
        responses.append((ChatTask.UnknownTask, "", "تاسك غير معروف."))

    return responses
