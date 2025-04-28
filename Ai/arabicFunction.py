from Ai.ArabicAi.ArabicTokenizer import ArabicTokenizers
from Ai.ArabicAi.Mapping import mapping
from Ai.ArabicAi.ArabicPreprocessor import ArabicPreprocessor
from Ai.ArabicAi.ReplyModule import replyModule
from Ai.ArabicAi.TaskProcessor import taskProcessor
from Ai.Recommendation.Arabic.ArabicReplyModuleRe import ArReplyModuleRe
from Ai.Recommendation.Arabic.ArabicCoursesystem import ArRecommendationSystem
from Ai.ArabicAi.chattask import ChatTask
from Data.dataStorage import DataStorage
from Ai.EnglishAi.Datastorage_DB import DatabaseStorage

ARmapper = mapping()
ARreply = replyModule()
ARproces = taskProcessor()
ARt = ArabicTokenizers()
ARp = ArabicPreprocessor()
recom_replyAr = ArReplyModuleRe()
data_storage = DatabaseStorage()
memory = DataStorage()
course_recommender = ArRecommendationSystem(data_storage, memory)

def langArabic(message, storage):
    try:
        corrected_message = ARt.normalize(message)
        ARtokens = ARt.tokenize(corrected_message)
        print("tokens: ", ARtokens)
        ARpos = ARt.pos_tag(ARtokens)
        print("pos: ", ARpos)
        ARtokens = ARp.preprocess(ARtokens)
        prev_data = storage.get_prev_data()

        print(f"[DEBUG] Current task before processing: {storage.get_current_task()}")
        s, options = "", []

        if storage.get_current_task() == "ExamRecom":
            print("[DEBUG] Continuing arabic Exam Recommendation Flow")
            s, options = recom_replyAr.recommender.handle_exam_recommendation(message)
            print(f"[DEBUG] Updated prev_data after response: {storage.get_prev_data()}")
            if s == "لا يوجد نظام امتحانات متاح لهذه المعلومات":
                return s, options, False
            if not options:
                storage.clear_data()
            return s, options, True
        elif storage.get_current_task() == "CourseSystem":
            print("[DEBUG] Continuing Course Recommendation Flow")
            s, options = course_recommender.receive_answer(message.strip())
            if ((s == "اسف لا يوجد اسئلة متاحة لهذا الكورس" and s == "لا يوجد اسم مادة هكذا") and
                    s == "يوجد خطا فى تنفيذ اجابتك , جرب مره اخرى"):
                return s, options, False
            if not options:
                storage.clear_data()
            return s, options, True

        else:
            ARtasks = ARmapper.mapToken(ARtokens, ARpos)
            print(f"[DEBUG] Identified tasks: {ARtasks}, type: {type(ARtasks)}")

            if all(task[0] == ChatTask.UnknownTask for task in ARtasks):
                print("[DEBUG] No valid recommendation task found, skipping recommendation.")
                return "I'm not sure how to answer that.", [], False
            else:
                if any(task[0] == ChatTask.ExamRecom for task in ARtasks):
                    print("[DEBUG] Handling Arabic Exam Recommendation Task")
                    storage.set_current_task("ExamRecom")
                    s, options = recom_replyAr.recommender.handle_exam_recommendation("")
                    return s, options, True
                if any(task[0] == ChatTask.courseSystem for task in ARtasks):
                    print("[DEBUG] Handling Course Recommendation Task")
                    storage.set_current_task("CourseSystem")
                    course_name = ARp.extract_course_name(ARtokens)
                    if course_name is not None:
                        print("===> " + course_name)
                    else:
                        print("===> No course name found.")
                    if course_name:
                        s, options = course_recommender.start_recommendation(course_name)
                    else:
                        s = "لا يوجد اسم مادة هكذا"
                    return s, options, True
            ARpre = ARproces.process(ARtasks, storage)
            print(f"[DEBUG] Processed tasks output: {ARpre}, type: {type(ARpre)}")
            response = ARreply.generate_response(ARpre)
            print(f"[DEBUG] Response received: {response}, Type: {type(response)}")
            if isinstance(response, tuple):
                s, options = response if len(response) == 2 else (response[0], [])
            else:
                s, options = response, []
        if not s:
            s = "انا اسف لا استطيع تنفيذ طلبك."
        if not options:
            options = []
        return s, options, False

    except Exception as e:
        return f"حدث خطأ أثناء معالجة العربية: {str(e)}"
