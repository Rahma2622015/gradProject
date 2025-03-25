from Ai.ArabicAi.chattask import ChatTask
from Data.dataStorage import DataStorage
class taskProcessor:

    def process(self, tasks:list[tuple[ChatTask,]],data:DataStorage)->list[tuple[ChatTask,]]:
        responses = []
        for task in tasks:
            if task[0] == ChatTask.StoreTask:
               if data.findName(task[1]):
                   responses.append((ChatTask.ContradactionTask,task[1],data.fetchValue(task[1]),task[1],task[2]))
               else:
                   data.addData(task[1],task[2])
                   responses.append((ChatTask.UnderstandingTask,task[1],task[2]))
            elif task[0] == ChatTask.LoadTask:
                responses.append((ChatTask.UnderstandingTask,task[1]))
            elif task[0] == ChatTask.GreetingTask:
                  if data.findName(task[1]):
                      responses.append((ChatTask.GreetingTask, data.fetchValue(task[1])))
                  else:
                      responses.append((ChatTask.GreetingTask,""))
            elif task[0]==ChatTask.CheckWellbeingTask:
                responses.append((ChatTask.CheckWellbeingTask,""))
            elif task[0]==ChatTask.MathTask:
                responses.append((ChatTask.MathTask,""))
            elif task[0] ==  ChatTask.QuestionTask:
                responses.append((ChatTask.UnderstandingTask,""))
            elif task[0] ==  ChatTask.ThanksTask:
                responses.append((ChatTask.ThanksTask,""))
            elif task[0] ==  ChatTask.HelpTask:
                responses.append((ChatTask.HelpTask,""))
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
            elif task[0] == ChatTask.askNameTask:
                    responses.append((ChatTask.askNameTask,data.fetchName(data.fetchValue(task[1]))))
            else:
                responses.append((ChatTask.UnknownTask,""))

        return  responses