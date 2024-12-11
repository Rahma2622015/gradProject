from Ai.replyTask import ReplyTask
from Ai.chattask import ChatTask
from Data.dataStorage import DataStorage
class TaskProcessor:

    def process(self, tasks:list[tuple[ChatTask,]],data:DataStorage)->list[tuple[ReplyTask,]]:
        responses = []
        for task in tasks:
            if task[0] == ChatTask.StoreTask:
               if data.findName(task[1]):
                   responses.append((ReplyTask.ContradactionTask,task[1],data.fetchValue(task[1]),task[1],task[2]))
               else:
                   data.addData(task[1],task[2])
                   responses.append((ReplyTask.UnderstandingTask,task[1],task[2]))
            elif task[0] == ChatTask.LoadTask:
                responses.append((ReplyTask.UnderstandingTask,task[1]))
            elif task[0] == ChatTask.GreetingTask:
                  if data.findName(task[1]):
                      responses.append((ReplyTask.Greeting, data.fetchValue(task[1])))
                  else:
                      responses.append((ReplyTask.Greeting,""))
            elif task[0]==ChatTask.CheckWellbeingTask:
                responses.append((ReplyTask.CheckWellbeing,""))
            elif task[0]==ChatTask.MathTask:
                responses.append((ReplyTask.Math,""))
            elif task[0] ==  ChatTask.QuestionTask:
                responses.append((ReplyTask.UnderstandingTask,""))
            elif task[0] ==  ChatTask.ThanksTask:
                responses.append((ReplyTask.Thanks,""))
            elif task[0] ==  ChatTask.HelpTask:
                responses.append((ReplyTask.Help,""))
            elif task[0] ==  ChatTask.GoodbyeTask:
                responses.append((ReplyTask.Goodbye,""))
            elif task[0] == ChatTask.ConfusionTask:
                responses.append((ReplyTask.Confusion, ""))
            elif task[0] == ChatTask.TypesOfProgramsTask:
                responses.append((ReplyTask.TypesOfPrograms, ""))
            elif task[0] == ChatTask.ExternalCoursesTask:
                responses.append((ReplyTask.ExternalCourses, ""))
            elif task[0] == ChatTask.DifficultyTask:
                responses.append((ReplyTask.Difficulty, ""))
            elif task[0] == ChatTask.HighGpaTask:
                responses.append((ReplyTask.HighGpa, ""))
            elif task[0] == ChatTask.MaterialsTypeTask:
                responses.append((ReplyTask.MaterialsType, ""))
            elif task[0] == ChatTask.chooseDepartment:
                responses.append((ReplyTask.chooseDep, ""))
            elif task[0] == ChatTask.academingtask:
                responses.append((ReplyTask.academingTask, ""))
            elif task[0] == ChatTask.classification:
                responses.append((ReplyTask.Classification, ""))
            elif task[0] == ChatTask.hours:
                responses.append((ReplyTask.hour, ""))
            elif task[0] == ChatTask.graduate:
                responses.append((ReplyTask.graduatation, ""))
            elif task[0] == ChatTask.enroll:
                responses.append((ReplyTask.enrollment, ""))
            else:
                responses.append((ReplyTask.UnknownTask,""))

        return  responses