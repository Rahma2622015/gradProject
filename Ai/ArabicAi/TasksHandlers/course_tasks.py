from Ai.EnglishAi.chattask import ChatTask
from Database.Datastorage_DB import DatabaseStorage

def handle_course_tasks(task, D: DatabaseStorage):
    responses = []

    course_name = None
    role = None
    task_words = task[1] if isinstance(task, tuple) and len(task) > 1 else task
    lowered_task = [w.lower().strip() for w in task_words]

    for i, word in enumerate(lowered_task):
        if word in ["درجة", "الدرجة", "الدرجات","درجات"]:
            course_name = " ".join(task_words[i + 1:])
            role = "درجة"
            break
        elif word in ["ساعة", "ساعات"]:
            course_name = " ".join(task_words[i + 1:])
            role = "ساعة"
            break
        elif word in ["متطلب", "متطلبات"]:
            course_name = " ".join(task_words[i + 1:])
            role = "متطلبات"
            break
        elif word in ["دكتور", "أستاذ", "مدرس","معيد"]:
            course_name = " ".join(task_words[i + 1:])
            role = "دكتور"
            break
        elif word in[ "القسم","قسم"]:
            course_name = " ".join(task_words[i + 1:])
            role = "قسم"
            break
        elif word in ["مادة", "موضوع", "درس"]:
            course_name = " ".join(task_words[i + 1:])
            role = "مادة"
            break

    if task[0] == ChatTask.CourseRoleQueryTask:
        if not course_name:
            responses.append((ChatTask.UnknownTask, "", "لم يتم تحديد اسم المادة."))
            return responses

        if role == "درجة":
            degree_val = D.courseDegree.get_course_degree(course_name,"ar")
            responses.append((ChatTask.CourseDegrees, course_name, degree_val or "درجة المادة غير موجودة."))

        elif role == "ساعة":
            hours = D.courseHour.get_course_hours(course_name,"ar")
            responses.append((ChatTask.CourseHours, course_name, hours or "ساعات المادة غير موجودة."))

        elif role == "متطلبات":
            pre = D.coursePre.get_course_prerequisite(course_name, 'ar')
            responses.append((ChatTask.PrerequisitesTask, course_name, pre or "متطلبات المادة غير موجودة."))

        elif role == "دكتور":
            prof = D.courseProfessor.get_professors_of_course(course_name, 'ar')
            ass = D.courseAssistant.get_assistants_of_course(course_name, 'ar')
            found = False

            if prof:
                found=True
                responses.append((ChatTask.ProfessorOfCourse, course_name, prof or "الدكتور غير موجود."))
            if ass:
                found=True
                responses.append((ChatTask.AssistantOfCourse, course_name, ass or "المعيد غير موجود."))
            if not found:
                responses.append(
                    (ChatTask.UnknownTask, course_name, "لا يوجد معلومات عن هذا الشخص لا كدكتور ولا كمعيد."))

        elif role == "قسم":
            dep = D.courseDepartment.get_department_of_course(course_name, 'ar')
            responses.append((ChatTask.DepartmentOfCourse, course_name, dep or "القسم غير موجود."))

        elif role == "مادة":
            desc = D.courseDes.get_course_description(course_name, 'ar')
            responses.append((ChatTask.CourseQueryTask, course_name, desc or "وصف المادة غير متاح."))

        else:
            responses.append((ChatTask.UnknownTask, course_name, "لم يتم التعرف على نوع السؤال."))

    else:
        responses.append((ChatTask.UnknownTask, "", "تاسك غير معروف."))

    return responses
