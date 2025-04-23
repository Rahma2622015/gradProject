from Ai.ArabicAi.chattask import ChatTask
from Data.dataStorage import DataStorage
from Ai.EnglishAi.Datastorage_DB import DatabaseStorage


class taskProcessor:

    def process(self, tasks:list[tuple[ChatTask,]], data:DataStorage)->list[tuple[ChatTask,]]:
        D = DatabaseStorage()
        responses = []
        name_from_greeting = None
        skip_store_response = False

        for task in tasks:
            if task[0] == ChatTask.GreetingTask and task[1]:
                name_from_greeting = task[1]

        for task in tasks:
            if task[0] == ChatTask.StoreTask and task[1] == "اسم" and task[2] == name_from_greeting:
                skip_store_response = True

        for task in tasks:
            if task[0] == ChatTask.GreetingTask:
                stored_name = data.fetchValue("اسم")
                if stored_name:
                    responses.append((ChatTask.GreetingTask, stored_name))
                else:
                    responses.append((ChatTask.GreetingTask, ""))

            elif task[0] == ChatTask.StoreTask:
                if data.findName(task[1]):
                    responses.append((ChatTask.ContradactionTask, task[1], data.fetchValue(task[1]), task[1], task[2]))
                else:
                    data.addData(task[1], task[2])
                    if not (skip_store_response and task[1] == "اسم" and task[2] == name_from_greeting):
                        responses.append((ChatTask.UnderstandingTask, task[1], task[2]))

            elif task[0] == ChatTask.askNameTask:
                stored_name = data.fetchValue("اسم")
                if stored_name:
                    responses.append((ChatTask.askNameTask, stored_name))
                else:
                    responses.append((ChatTask.askNameTask, ""))


            elif task[0] == ChatTask.LoadTask:
                responses.append((ChatTask.UnderstandingTask,task[1]))
            elif task[0]==ChatTask.CheckWellbeingTask:
                responses.append((ChatTask.CheckWellbeingTask,""))
            elif task[0]==ChatTask.MathTask:
                responses.append((ChatTask.MathTask,""))
            elif task[0] ==  ChatTask.QuestionTask:
                responses.append((ChatTask.UnderstandingTask,""))
            elif task[0] ==  ChatTask.ThanksTask:
                responses.append((ChatTask.ThanksTask,""))
            elif task[0] ==  ChatTask.askHelpingTask:
                responses.append((ChatTask.askHelpingTask,""))
            elif task[0] ==  ChatTask.GoodbyeTask:
                responses.append(( ChatTask.GoodbyeTask,""))
            elif task[0] == ChatTask.ConfusionTask:
                responses.append(( ChatTask.ConfusionTask, ""))
            elif task[0] == ChatTask.TypesOfProgramsTask:
                responses.append((ChatTask.TypesOfProgramsTask, ""))
            elif task[0] == ChatTask.ExternalCoursesTask:
                responses.append((ChatTask.ExternalCoursesTask, ""))
            elif task[0] == ChatTask.DifficultyTask:
                responses.append((ChatTask.DifficultyTask, ""))
            elif task[0] == ChatTask.HighGpaTask:
                responses.append((ChatTask.HighGpaTask, ""))
            elif task[0] == ChatTask.MaterialsTypeTask:
                responses.append(( ChatTask.MaterialsTypeTask, ""))
            elif task[0] == ChatTask.ChooseDepartmentTask:
                responses.append(( ChatTask.ChooseDepartmentTask, ""))
            elif task[0] == ChatTask.AcademicAdvisorTask:
                responses.append(( ChatTask.AcademicAdvisorTask, ""))
            elif task[0] == ChatTask.ClassificationTask:
                responses.append(( ChatTask.ClassificationTask, ""))
            elif task[0] == ChatTask.CreditHoursTask:
                responses.append((ChatTask.CreditHoursTask, ""))
            elif task[0] == ChatTask.GraduationTask:
                responses.append((ChatTask.GraduationTask, ""))
            elif task[0] == ChatTask.EnrollmentTask:
                responses.append(( ChatTask.EnrollmentTask, ""))
            elif task[0] == ChatTask.askHelpingTask:
                responses.append((ChatTask.askHelpingTask, ""))
            elif task[0] == ChatTask.ExamRecom:
                responses.append((ChatTask.ExamRecom, ""))
            elif task[0] == ChatTask.ProfessorQueryTask:
                professor_name = None
                keywords = ["استاذ", "دكتور"]
                task_words = task[1] if isinstance(task, tuple) and len(task) > 1 else task
                for i, word in enumerate(task_words):
                    if word.lower().strip() in keywords:
                        professor_name = " ".join(task_words[i + 1:])
                        print("🔍 Extracted name:", professor_name)
                        break
                if professor_name:
                    # ---------
                    professor_info = D.get_professor_info_arabic(str(professor_name))
                else:
                    professor_name = "Unknown"
                    professor_info = "No information available"

                responses.append((ChatTask.ProfessorQueryTask, professor_name, professor_info))

            elif task[0] == ChatTask.CourseQueryTask:
                course_name = ""
                keywords = ["مادة", "موضوع", "درس", "مقرر"]
                task_words = task[1] if isinstance(task, tuple) and len(task) > 1 else task

                for i, word in enumerate(task_words):
                    if word in keywords:
                        course_name = " ".join(task_words[i + 1:])
                        print("🔍 Extracted cname:", course_name)
                        break

                try:
                    course_info = D.get_course_description_arabic(course_name)
                    if not course_info or course_info.strip() == "Course not found.":
                        course_info = f"Sorry, the course '{course_name}' is not found in our database."
                except Exception as e:
                    print("❌ Error while getting course info:", str(e))
                    course_info = "There was an error while fetching the course description."

                responses.append((ChatTask.CourseQueryTask, course_name, course_info))

            elif task[0] == ChatTask.PrerequisiteQueryTask:
                course_name = ""
                keywords = ["مادة", "موضوع", "درس", "مقرر","متطلب", "متطلبات", "شرط", "شروط", "مطلوب", "ضروري", "معتمد", "معتمده" ,"معتمدة"]
                task_words = task[1] if isinstance(task, tuple) and len(task) > 1 else task

                for i, word in enumerate(task_words):
                    if word in keywords:
                        course_name = " ".join(task_words[i + 1:])
                        print("🔍 Extracted pname:", course_name)
                        break

                try:
                    course_info = D.get_course_prerequisite_arabic(course_name)
                    if not course_info or course_info.strip() == "Course not found.":
                        course_info = f"Sorry, the course '{course_name}' is not found in our database."
                except Exception as e:
                    print("❌ Error while getting course pre:", str(e))
                    course_info = "There was an error while fetching the course description."

                responses.append((ChatTask.CourseQueryTask, course_name, course_info))

            else:
                responses.append((ChatTask.UnknownTask,""))

        return  responses