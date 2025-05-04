from Ai.ArabicAi.chattask import ChatTask


def handle_basic_tasks(task, data, skip_store_response, name_from_greeting):
    responses = []
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

    return responses
