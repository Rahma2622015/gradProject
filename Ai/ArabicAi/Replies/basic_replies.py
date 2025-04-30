from Ai.ArabicAi.chattask import ChatTask
from random import choice

def handle_basic_reply(r, data):
    if r[0] == ChatTask.GreetingTask:
        return choice(data.get("GreetingWithName", [])).format(x=r[1]) if r[1] else choice(data.get("Greeting", []))
    elif r[0] == ChatTask.UnderstandingTask:
        return choice(data.get("Understanding", [])).format(x=r[2])
    elif r[0] == ChatTask.askNameTask:
        return choice(data.get("reply_name", [])).format(x=r[1]) if r[1] else choice(data.get("reply", []))
    elif r[0] == ChatTask.ContradactionTask:
        return choice(data.get("Contradiction", [])).format(y=r[2])
    elif r[0] == ChatTask.CheckWellbeingTask:
        return choice(data.get("CheckWellbeing", []))
    elif r[0] == ChatTask.ThanksTask:
        return choice(data.get("ThanksReplies", []))
    elif r[0] == ChatTask.askHelpingTask:
        return choice(data.get("askhelp", []))
    elif r[0] == ChatTask.GoodbyeTask:
        return choice(data.get("Goodbye", []))
    elif r[0] == ChatTask.ConfusionTask:
        return choice(data.get("ConfusionReplies", []))
    else:
        return choice(data.get("Unknown", []))
