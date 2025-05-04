from .initialization import *
from .task_continuation import handle_exam_recom, handle_course_system, handle_multi_course
from .task_detection import detect_tasks
from Ai.ArabicAi.chattask import ChatTask

def langArabic(message, storage):
    try:
        corrected_message = ARt.normalize(message)
        ARtokens = ARt.tokenize(corrected_message)
        ARpos = ARt.pos_tag(ARtokens)
        ARtokens = ARp.preprocess(ARtokens)
        prev_data = storage.get_prev_data()
        print("tokenr ",ARtokens)
        print("posr ",ARpos)

        if storage.get_current_task() == "ExamRecom":
            return handle_exam_recom(storage, recom_replyAr, message)

        elif storage.get_current_task() == "CourseSystem":
            return handle_course_system(storage, course_recommender, message)

        elif storage.get_current_task() == "MultiCourseSystem":
            return handle_multi_course(storage, recom_replyAr, ARp, message)

        else:
            ARtasks = detect_tasks(ARtokens, ARpos, use_semantic_armapper, ARmapper, mapper)
            if all(task[0] == ChatTask.UnknownTask for task in ARtasks):
                return "I'm not sure how to answer that.", [], False

            if any(task[0] == ChatTask.ExamRecom for task in ARtasks):
                storage.set_current_task("ExamRecom")
                return recom_replyAr.recommender.handle_exam_recommendation("")

            if any(task[0] == ChatTask.courseSystem for task in ARtasks):
                storage.set_current_task("CourseSystem")
                course_name = ARp.extract_course_name(ARtokens)
                if course_name:
                    return course_recommender.start_recommendation(course_name)
                else:
                    return "لا يوجد اسم مادة هكذا", [], True

            if any(task[0] == ChatTask.MultiCourseRecommendationTask for task in ARtasks):
                storage.set_current_task("MultiCourseSystem")
                course_names = ARp.extract_all_course_names(corrected_message)
                storage.save_data("all_courses", course_names)
                if course_names:
                    response, options = recom_replyAr.course_selection_recommender.start(course_names)
                    s = response if isinstance(response, str) else "Error processing multi-course recommendation."
                    return s, options, True
                else:
                    return "Sorry, I couldn't detect the course names from your question.", [], True

            ARpre = ARproces.process(ARtasks, storage)
            response = ARreply.generate_response(ARpre)
            if isinstance(response, tuple):
                return response if len(response) == 2 else (response[0], [], False)
            return response, [], False

    except Exception as e:
        return f"حدث خطأ أثناء معالجة العربية: {str(e)}", [], False
