# Ai.EnglishReceving.intent_detector.py

from Ai.EnglishAi.chattask import ChatTask

def detect_intent(tasks, storage, corrected_message, t):
    if any(task[0] == ChatTask.ExamSystem for task in tasks):
        storage.set_current_task("ExamSystem")
        return "ExamSystem", ""

    if any(task[0] == ChatTask.CourseSystem for task in tasks):
        storage.set_current_task("CourseSystem")
        return "CourseSystem", corrected_message

    if any(task[0] == ChatTask.MultiCourseRecommendationTask for task in tasks):
        storage.set_current_task("MultiCourseSystem")
        course_names = t.extract_all_course_names(corrected_message)
        storage.save_data("all_courses", course_names)
        return "MultiCourseSystem", corrected_message

    return "General", None
