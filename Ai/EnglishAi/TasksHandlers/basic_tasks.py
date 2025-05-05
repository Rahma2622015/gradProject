from Ai.EnglishAi.chattask import ChatTask

def handle_basic_tasks(task, data):
    responses = []
    if task[0] == ChatTask.StoreTask:
        if data.findName(task[1]):
            responses.append((ChatTask.ContradictionTask, task[1], data.fetchValue(task[1]), task[1], task[2]))
        else:
            data.addData(task[1], task[2])
            responses.append((ChatTask.UnderstandingTask, task[1], task[2]))

    elif task[0] == ChatTask.LoadTask:
        responses.append((ChatTask.UnderstandingTask, task[1]))

    elif task[0] == ChatTask.GreetingTask:
        if data.findName(task[1]):
            responses.append((ChatTask.GreetingTask, data.fetchValue(task[1])))
        else:
            responses.append((ChatTask.GreetingTask, ""))

    elif task[0] == ChatTask.AskNameTask:
        name = data.fetchValue("name")
        if name:
            responses.append((ChatTask.AskNameTask, name))
        else:
            responses.append((ChatTask.AskNameTask, "I can't remember your name, could you tell me it? "))
    return responses
