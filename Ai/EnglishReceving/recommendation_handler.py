
def handle_exam_recommendation(storage, recom_reply, message):
    s, options = recom_reply.recommender.handle_exam_recommendation(message)
    if s == "No exam data available for this subject.":
        storage.clear_data()
        return s, options, False
    if not options:
        storage.clear_data()
    return s, options, True


def handle_course_recommendation(storage, course_recommender, tokenizer, message):
    course_name = tokenizer.extract_course_name(message)
    if course_name:
        s, options = course_recommender.start_recommendation(course_name)
    else:
        s = "Please mention a valid course name so I can recommend suitable subjects."
        options = []
    return s, options, True


def handle_multi_course_recommendation(storage, recom_reply, tokenizer, message):
    prev_data = storage.get_prev_data()
    if not prev_data.get("all_courses"):
        course_names = tokenizer.extract_all_course_names(message)
        if course_names:
            response, options = recom_reply.course_selection_recommender.start(course_names)
            s = response if isinstance(response, str) else "Error processing multi-course recommendation."
        else:
            s = "Sorry, I couldn't detect the course names from your question."
            options = []
    else:
        s, options = recom_reply.course_selection_recommender.handle_answer(message)
    return s, options, True
