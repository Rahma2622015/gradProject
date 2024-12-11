from Ai.ReplyTask import ReplyTask
from random import choice
from Ai.ResponsesData import ResponseData

class ReplyModule:
    def __init__(self):
        self.Greeting = ResponseData.Greeting
        self.Understanding = ResponseData.Understanding
        self.Contradaction = ResponseData.Contradaction
        self.CheckWellbeing = ResponseData.CheckWellbeing
        self.Mathh = ResponseData.Matht
        self.ThanksReplies = ResponseData.ThanksReplies
        self.ConfusionReplies = ResponseData.ConfusionReplies
        self.askHelping = ResponseData.askHelping
        self.Goodbyee = ResponseData.Goodbyee
        self.programs=ResponseData.Programs
        self.courses=ResponseData.ExternalCourses
        self.Difficult=ResponseData.Difficulty
        self.Highgpa=ResponseData.HighGpa
        self.Materiatype=ResponseData.MaterialType
        self.chooseDepartment = ResponseData.chooseD
        self.academic = ResponseData.acad
        self.classification = ResponseData.classfy
        self.hours = ResponseData.hou
        self.graduation = ResponseData.grad
        self.enrollment = ResponseData.enroll
        self.unknow = ResponseData.Unknown
        self.askhelp = ResponseData.askhelp
        self.Askname = ResponseData.replay_name

    def generate_response(self, reply: list[tuple[ReplyTask,]]) -> str:
        s = ""
        for r in reply:
            if r[0] == ReplyTask.Greeting:
                s += "\n" + choice(self.Greeting).format(x=r[1])
            elif r[0] == ReplyTask.UnderstandingTask:
                s += "\n" + choice(self.Understanding).format(x=r[2])
            elif r[0] == ReplyTask.askNamee:
                s += "\n" + choice(self.Askname).format(x=r[1])
            elif r[0] == ReplyTask.ContradactionTask:
                s += "\n" + choice(self.Contradaction).format(y=r[2])
            elif r[0] == ReplyTask.CheckWellbeing:
                s += "\n" + choice(self.CheckWellbeing)
            elif r[0] == ReplyTask.Thanks:
                s += "\n" + choice(self.ThanksReplies)
            elif r[0] == ReplyTask.Help:
                s += "\n" + choice(self.askHelping)
            elif r[0] == ReplyTask.Goodbye:
                s += "\n" + choice(self.Goodbyee)
            elif r[0] == ReplyTask.Confusion:
                s += "\n" + choice(self.ConfusionReplies)
            elif r[0] == ReplyTask.Help:
                s += "\n" + choice(self.askHelping)
             #end trivial   
            elif r[0] == ReplyTask.TypesOfPrograms:
                s += "\n" + choice(self.programs)
            elif r[0] == ReplyTask.Math:
                s += "\n" + choice(self.Mathh)
            elif r[0] == ReplyTask.ExternalCourses:
                s += "\n" + choice(self.courses)
            elif r[0] == ReplyTask.Difficulty:
                s += "\n" + choice(self.Difficult)
            elif r[0] == ReplyTask.HighGpa:
                s += "\n" + choice(self.Highgpa)
            elif r[0] == ReplyTask.MaterialsType:
                s += "\n" + choice(self.Materiatype)
            elif r[0] == ReplyTask.chooseDep:
                s += "\n" + choice(self.chooseDepartment)
            elif r[0] == ReplyTask.academingTask:
                s += "\n" + choice(self.academic)
            elif r[0] == ReplyTask.Classification:
                s += "\n" + choice(self.classification)
            elif r[0] == ReplyTask.hour:
                s += "\n" + choice(self.hours)
            elif r[0] == ReplyTask.graduatation:
                s += "\n" + choice(self.graduation)
            elif r[0] == ReplyTask.enrollment:
                s += "\n" + choice(self.enrollment)
            else:
                s += "\n" + choice(self.unknow)

        return s