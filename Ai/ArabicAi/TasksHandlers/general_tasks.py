from Ai.ArabicAi.chattask import ChatTask

def handle_general_tasks(task):
    responses = []
    task_type = task[0]
    responses.append((task_type, ""))
    return responses
