# Ai.EnglishReceving.langEnglish.py

from Ai.EnglishReceving.initialization import (
    f, grammer, m, mapper, trivial_mapper, reply, proces,
    t, p, a, recom_reply, bigram_model,
    course_recommender, use_semantic_mapperfun
)
from Ai.EnglishAi.chattask import ChatTask
from Ai.EnglishReceving.task_router import route_current_task
from Ai.EnglishReceving.intent_detector import detect_intent
from Ai.EnglishReceving.task_mapper_engine import map_tasks

def langEnglish(message, storage):
    try:
        message_lower = p.lowercase(message)
        corrected_message = a.correct_text(message_lower)
        tokens = t.tokenize(corrected_message)
        pos = t.pos_tag(tokens)
        print("tokens ", tokens)
        print("pos ", pos)
        if not use_semantic_mapperfun():
            tokens = p.preprocess(tokens, pos)

        current_task = storage.get_current_task()
        print(f"[DEBUG] Current task before processing: {current_task}")

        if current_task in ["ExamSystem", "CourseSystem", "MultiCourseSystem"]:
            print("task-type: ",current_task)
            return route_current_task(current_task, storage, recom_reply, course_recommender, t, message)

        tasks = map_tasks(tokens, pos, f, bigram_model, trivial_mapper, grammer, use_semantic_mapperfun, mapper, m)
        print(f"[DEBUG] Identified tasks: {tasks}, type: {type(tasks)}")

        if all(task[0] == ChatTask.UnknownTask for task in tasks):
            print("task-type: ",current_task)
            return "I'm not sure how to answer that.", [], False

        intent, new_message = detect_intent(tasks, storage, corrected_message, t)
        if intent != "General":
            return route_current_task(intent, storage, recom_reply, course_recommender, t, new_message)

        print("task-type: ",current_task)
        processed_tasks = proces.process(tasks, storage)
        print(f"[DEBUG] Processed tasks output: {processed_tasks}, type: {type(processed_tasks)}")

        response = reply.generate_response(processed_tasks)
        print(f"[DEBUG] Response received: {response}, Type: {type(response)}")

        if isinstance(response, tuple):
            s, options = response if len(response) == 2 else (response[0], [])
        else:
            s, options = response, []

        if not s:
            s = "I'm sorry, I couldn't process your request."
        if not options:
            options = []

        return s, options, False

    except Exception as e:
        return f"Error in English processing: {str(e)}", [], False
