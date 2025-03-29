from Ai.EnglishAi.ReplyTask import ReplyTask
from Ai.EnglishAi.chattask import ChatTask
from Data.dataStorage import DataStorage
class TaskProcessor:

    def process(self, tasks:list[tuple[ChatTask,]],data:DataStorage)->list[tuple[ReplyTask,]]:
        responses = []

        for task in tasks:
            task_enum = task[0]
            if isinstance(task_enum, ChatTask):
                task_string = task_enum.name
            if task_enum == ChatTask.StoreTask:
               if data.findName(task[1]):
                   responses.append((ReplyTask.ContradictionTask,task[1],data.fetchValue(task[1]),task[1],task[2]))
               else:
                   data.addData(task[1],task[2])
                   responses.append((ReplyTask.UnderstandingTask,task[1],task[2]))
            elif task_enum == ChatTask.LoadTask:
                responses.append((ReplyTask.UnderstandingTask,task[1]))
            elif task_enum== ChatTask.GreetingTask:
                  if data.findName(task[1]):
                      responses.append((ReplyTask.Greeting, data.fetchValue(task[1])))
                  else:
                      responses.append((ReplyTask.Greeting,""))
            elif task_enum == ChatTask.AskNameTask:
                    responses.append((ReplyTask.AskName,data.fetchValue("name")))
            elif task_enum==ChatTask.CheckWellbeingTask:
                responses.append((ReplyTask.CheckWellbeing,""))
            elif task_enum==ChatTask.MathTask:
                responses.append((ReplyTask.Math,""))
            elif task_enum ==  ChatTask.QuestionTask:
                responses.append((ReplyTask.UnderstandingTask,""))
            elif task_enum ==  ChatTask.ThanksTask:
                responses.append((ReplyTask.Thanks,""))
            elif task_enum ==  ChatTask.HelpTask:
                responses.append((ReplyTask.Help,""))
            elif task_enum ==  ChatTask.GoodbyeTask:
                responses.append((ReplyTask.Goodbye,""))
            elif task_enum == ChatTask.ConfusionTask:
                responses.append((ReplyTask.Confusion, ""))
            elif task_enum == ChatTask.TypesOfProgramsTask:
                responses.append((ReplyTask.TypesOfPrograms, ""))
            elif task_enum == ChatTask.ExternalCoursesTask:
                responses.append((ReplyTask.ExternalCourses, ""))
            elif task_enum== ChatTask.DifficultyTask:
                responses.append((ReplyTask.Difficulty, ""))
            elif task_enum == ChatTask.HighGpaTask:
                responses.append((ReplyTask.HighGpa, ""))
            elif task_enum == ChatTask.MaterialsTypeTask:
                responses.append((ReplyTask.MaterialsType, ""))
            elif task_enum == ChatTask.ChooseDepartmentTask:
                responses.append((ReplyTask.ChooseDepartment, ""))
            elif task_enum == ChatTask.AcademicAdvisorTask:
                responses.append((ReplyTask.AcademicAdvisorTask, ""))
            elif task_enum == ChatTask.ClassificationTask:
                responses.append((ReplyTask.ClassificationTask, ""))
            elif task_enum == ChatTask.CreditHoursTask:
                responses.append((ReplyTask.CreditHours, ""))
            elif task_enum == ChatTask.GraduationTask:
                responses.append((ReplyTask.Graduation, ""))
            elif task_enum == ChatTask.EnrollmentTask:
                responses.append((ReplyTask.Enrollment, ""))
            elif task_enum == ChatTask.AskHelpingTask:
                responses.append((ReplyTask.AskHelp, ""))
            elif task_enum == ChatTask.ExamSystem:
                responses.append((ReplyTask.ExamSystem, ""))
                print(f"[DEBUG] Task {task_enum} added to responses.")
            else:
                responses.append((ReplyTask.UnknownTask,""))

        return  responses