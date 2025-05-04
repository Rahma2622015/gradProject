# Ai.EnglishReceving.task_router.py

from Ai.EnglishReceving.recommendation_handler import (
    handle_exam_recommendation,
    handle_course_recommendation,
    handle_multi_course_recommendation
)

def route_current_task(task, storage, recom_reply, course_recommender, t, message):
    if task == "ExamSystem":
        return handle_exam_recommendation(storage, recom_reply, message)
    elif task == "CourseSystem":
        return handle_course_recommendation(storage, course_recommender, t, message)
    elif task == "MultiCourseSystem":
        return handle_multi_course_recommendation(storage, recom_reply, t, message)
    return "Invalid task context", [], False
