from Ai.ArabicAi.chattask import ChatTask
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

    lowered_task = [w.lower().strip() for w in task_words]
    for i, word in enumerate(lowered_task):
        if word in ["درجة", "الدرجة", "الدرجات","درجات"]:
            next_words = task_words[i + 1:]
            found_course = False
            for j, word in enumerate(next_words):
                if word in ["مادة", "موضوع", "درس"]:
                    course_name = " ".join(next_words[j + 1:])
                    role = "درجة"
                    found_course = True
                    break
            if not found_course:
                course_name = " ".join(next_words)
                role = "درجة"
            break

        elif word in ["ساعة", "ساعات"]:
            next_words = task_words[i + 1:]
            found_course = False
            for j, word in enumerate(next_words):
                if word in ["مادة", "موضوع", "درس"]:
                    course_name = " ".join(next_words[j + 1:])
                    role = "ساعة"
                    found_course = True
                    break
            if not found_course:
                course_name = " ".join(next_words)
                role = "ساعة"
            break

        elif word in ["متطلب", "متطلبات"]:
            next_words = task_words[i + 1:]
            found_course = False
            for j, word in enumerate(next_words):
                if word in ["مادة", "موضوع", "درس"]:
                    course_name = " ".join(next_words[j + 1:])
                    role = "متطلبات"
                    found_course = True
                    break
            if not found_course:
                course_name = " ".join(next_words)
                role = "متطلبات"
            break

        elif word in[ "القسم","برنامج","قسم"]:
            next_words = task_words[i + 1:]
            found_course = False
            for j, word in enumerate(next_words):
                if word in ["مادة", "موضوع", "درس"]:
                    course_name = " ".join(next_words[j + 1:])
                    role = "قسم"
                    found_course = True
                    break
            if not found_course:
                course_name = " ".join(next_words)
                role = "قسم"
            break

        elif word in[ "دكتور","أستاذ","د","د.","مدرس"]:
            person_name = " ".join(task_words[i + 1:])
            role = "دكتور"
            break

        elif word in ["مادة", "درس", "موضوع"]:
            next_words = task_words[i + 1:]  # قائمة من الكلمات بعد "مادة"
            found_doctor = False
            for j, w in enumerate(next_words):
                if w in ["دكتور", "أستاذ", "د", "د.", "مدرس"]:
                    person_name = " ".join(next_words[j + 1:])
                    role = "دكتور"
                    found_doctor = True
                    break
            if not found_doctor:
                course_name = " ".join(next_words)
                role = "مادة"
            break


    print("rr",role ," cname",course_name," pname ",person_name)


    if task[0] == ChatTask.CourseRoleQueryTask:
        try:
            if role == "درجة" and course_name:
                val = degree.get_course_degree(course_name)
                responses.append((ChatTask.CourseDegrees, course_name, val))


            elif role == "ساعة" and course_name:
                val = hour.get_course_hours(course_name)
                responses.append((ChatTask.CourseHours, course_name, val))

            elif role == "متطلبات" and course_name:
                val = prerequisite.get_course_prerequisite(course_name,"ar")
                if val:
                    responses.append((ChatTask.PrerequisiteQueryTask, course_name, val))
                else:
                    responses.append((ChatTask.PrerequisiteQueryTask,course_name,"لا يوجد متطلبات لهذه المادة"))

            elif role == "دكتور" and person_name:
                val_prof = course_of_prof.get_courses_of_professor(person_name,"ar")
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
                    responses.append((ChatTask.UnknownTask, person_name, "لا يوجد معلومات كافية"))

            elif role == "قسم" and course_name:
                val = dep_of_course.get_department_of_course(course_name,"ar")
                responses.append((ChatTask.DepartmentOfCourse, course_name, val))

            elif role == "مادة" and course_name:
                val = description.get_course_description(course_name,"ar")

                responses.append((ChatTask.CourseQueryTask, val))

            else:
                responses.append(
                    (ChatTask.UnknownTask, course_name or person_name, "هذا السؤال لا استطيع فهمه"))

        except Exception as e:
            responses.append((ChatTask.UnknownTask, course_name or person_name, f"هناك خطأ: {str(e)}"))

    else:
        responses.append((ChatTask.UnknownTask, "", "مهمه غير مدعومه."))

    return responses