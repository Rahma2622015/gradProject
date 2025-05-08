from random import choice
from Ai.EnglishAi.chattask import ChatTask

def handle_basic_tasks(r, data):
    if r[0] == ChatTask.GreetingTask:
        return choice(data.get("Greeting", [])).format(x=r[1])
    elif r[0] == ChatTask.UnderstandingTask:
        return choice(data.get("Understanding", [])).format(x=r[2])
    elif r[0] == ChatTask.AskNameTask:
        return choice(data.get("replay_name", [])).format(x=r[1])
    elif r[0] == ChatTask.ContradictionTask:
        return choice(data.get("Contradiction", [])).format(y=r[2])
    elif r[0] == ChatTask.CheckWellbeingTask:
        return choice(data.get("CheckWellbeing", []))
    elif r[0] == ChatTask.ThanksTask:
        return choice(data.get("ThanksReplies", []))
    elif r[0] == ChatTask.AskHelpingTask:
        return choice(data.get("askhelp", []))
    elif r[0] == ChatTask.GoodbyeTask:
        return choice(data.get("Goodbye", []))
    elif r[0] == ChatTask.ConfusionTask:
        return choice(data.get("ConfusionReplies", []))
    return None