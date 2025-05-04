
def handle_exam_recom(storage, recom_replyAr, message):
    s, options = recom_replyAr.recommender.handle_exam_recommendation(message)
    if s == "لا يوجد نظام امتحانات متاح لهذه المعلومات":
        return s, options, False
    if not options:
        storage.clear_data()
    return s, options, True


def handle_course_system(storage, course_recommender, message):
    s, options = course_recommender.receive_answer(message.strip())
    if s in ["اسف لا يوجد اسئلة متاحة لهذا الكورس", "لا يوجد اسم مادة هكذا", "يوجد خطا فى تنفيذ اجابتك , جرب مره اخرى"]:
        return s, options, False
    if not options:
        storage.clear_data()
    return s, options, True


def handle_multi_course(storage, recom_replyAr, ARp, message):
    prev_data = storage.get_prev_data()
    if not prev_data.get("all_courses"):
        course_names = ARp.extract_all_course_names(message)
        if course_names:
            response, options = recom_replyAr.course_selection_recommender.start(course_names)
            s = response if isinstance(response, str) else "Error processing multi-course recommendation."
        else:
            s = "Sorry, I couldn't detect the course names from your question."
    else:
        s, options = recom_replyAr.course_selection_recommender.handle_answer(message)
    return s, options, True
