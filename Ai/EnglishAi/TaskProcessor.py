from Ai.EnglishAi.chattask import ChatTask
from Ai.EnglishAi.Datastorage_DB import Data_Storage
from Data import DataStorage

class TaskProcessor:
    def process(self, tasks:list[tuple[ChatTask,]],data:DataStorage)->list[tuple[ChatTask,]]:
        responses = []
        D=Data_Storage()
        for task in tasks:
            task_enum = task[0]
            if isinstance(task_enum, ChatTask):
                task_string = task_enum.name
            if task_enum == ChatTask.StoreTask:
               if data.findName(task[1]):
                   responses.append((ChatTask.ContradictionTask,task[1],data.fetchValue(task[1]),task[1],task[2]))
               else:
                   data.addData(task[1],task[2])
                   responses.append((ChatTask.UnderstandingTask,task[1],task[2]))
            elif task_enum == ChatTask.LoadTask:
                responses.append((ChatTask.UnderstandingTask,task[1]))
            elif task_enum== ChatTask.GreetingTask:
                  if data.findName(task[1]):
                      responses.append((ChatTask.GreetingTask, data.fetchValue(task[1])))
                  else:
                      responses.append((ChatTask.GreetingTask,""))
            elif task_enum==ChatTask.CheckWellbeingTask:
                responses.append((ChatTask.CheckWellbeingTask,""))
            elif task_enum==ChatTask.MathTask:
                responses.append((ChatTask.MathTask,""))
            elif task_enum ==  ChatTask.QuestionTask:
                responses.append((ChatTask.UnderstandingTask,""))
            elif task_enum ==  ChatTask.ThanksTask:
                responses.append((ChatTask.ThanksTask,""))
            elif task_enum ==  ChatTask.HelpTask:
                responses.append((ChatTask.HelpTask,""))
            elif task_enum ==  ChatTask.GoodbyeTask:
                responses.append((ChatTask.GoodbyeTask,""))
            elif task_enum == ChatTask.ConfusionTask:
                responses.append((ChatTask.ConfusionTask, ""))
            elif task_enum == ChatTask.TypesOfProgramsTask:
                responses.append((ChatTask.TypesOfProgramsTask, ""))
            elif task_enum == ChatTask.ExternalCoursesTask:
                responses.append((ChatTask.ExternalCoursesTask, ""))
            elif task_enum== ChatTask.DifficultyTask:
                responses.append((ChatTask.DifficultyTask, ""))
            elif task_enum == ChatTask.HighGpaTask:
                responses.append((ChatTask.HighGpaTask, ""))
            elif task_enum == ChatTask.MaterialsTypeTask:
                responses.append(( ChatTask.MaterialsTypeTask, ""))
            elif task_enum == ChatTask.ChooseDepartmentTask:
                responses.append((ChatTask.ChooseDepartmentTask, ""))
            elif task_enum == ChatTask.AcademicAdvisorTask:
                responses.append((ChatTask.AcademicAdvisorTask, ""))
            elif task_enum == ChatTask.ClassificationTask:
                responses.append((ChatTask.ClassificationTask, ""))
            elif task_enum == ChatTask.CreditHoursTask:
                responses.append((ChatTask.CreditHoursTask, ""))
            elif task_enum == ChatTask.GraduationTask:
                responses.append(( ChatTask.GraduationTask, ""))
            elif task_enum == ChatTask.EnrollmentTask:
                responses.append(( ChatTask.EnrollmentTask, ""))
            elif task_enum == ChatTask.AskHelpingTask:
                responses.append((ChatTask.AskHelpingTask, ""))
            elif task_enum == ChatTask.AskNameTask:
                responses.append((ChatTask.AskNameTask,data.fetchName(data.fetchValue(task[1]))))

            elif task_enum == ChatTask.ExamSystem:
                responses.append((ChatTask.ExamSystem, ""))

            elif task_enum == ChatTask.ProfessorQueryTask:
                professor_name = None
                keywords = ["professor", "dr."]
                task_words = task[1] if isinstance(task, tuple) and len(task) > 1 else task
                for i, word in enumerate(task_words):
                    if word.lower().strip() in keywords and i + 1 < len(task_words):
                        professor_name = task_words[i + 1] + " " + task_words[i + 2]
                        print("🔍 Extracted name:", professor_name)
                        break
                if professor_name :
                    professor_info = D.get_professor_info(str(professor_name))
                else:
                    professor_name = "Unknown"
                    professor_info = "No information available"

                responses.append((ChatTask.ProfessorQueryTask, professor_name, professor_info))

            elif task_enum == ChatTask.CourseQueryTask:
                course_name = ""
                keywords = ["course", "subject", "lesson"]
                task_words = task[1] if isinstance(task, tuple) and len(task) > 1 else task

                for i, word in enumerate(task_words):
                    if word in keywords and i + 1 < len(task_words):
                        course_name = " ".join(task_words[i + 1:])
                        print("🔍 Extracted cname:", course_name)
                        break

                try:
                    print("1")
                    course_info = D.get_course_description(course_name)
                    if not course_info or course_info.strip() == "Course not found.":
                        print("2")
                        course_info = f"Sorry, the course '{course_name}' is not found in our database."
                except Exception as e:
                    print("❌ Error while getting course info:", str(e))
                    course_info = "There was an error while fetching the course description."

                responses.append((ChatTask.CourseQueryTask, course_name, course_info))

            else:
                responses.append((ChatTask.UnknownTask,""))

        return  responses