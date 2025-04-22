from Ai.ArabicAi.ArabicTokenizer import ArabicTokenizers
from Ai.ArabicAi.Mapping import mapping
from Ai.ArabicAi.ArabicPreprocessor import ArabicPreprocessor
from Ai.ArabicAi.ReplyModule import replyModule
from Ai.ArabicAi.TaskProcessor import taskProcessor
from Ai.Recommendation.Arabic.ArabicReplyModuleRe import ArReplyModuleRe
from Ai.Recommendation.Arabic.ArabicRecomExamSystem import ArRecommendation
from Ai.ArabicAi.chattask import ChatTask

ARmapper = mapping()
ARreply = replyModule()
ARproces = taskProcessor()
ARt = ArabicTokenizers()
ARp = ArabicPreprocessor()
recom_replyAr = ArReplyModuleRe()
def langArabic(message, storage, user_id):
    try:
        ARtokens = ARt.tokenize(message)
        print("tokens: ",ARtokens)
        ARpos = ARt.pos_tag(ARtokens)
        print("pos: ",ARpos)
        ARtokens = ARp.preprocess(ARtokens)
        prev_data = storage.get_prev_data(user_id)

        print(f"[DEBUG] Current task before processing: {storage.get_current_task(user_id)}")
        s, options = "", []

        if storage.get_current_task(user_id) == "ExamRecom":
            print("[DEBUG] Continuing arabic Exam Recommendation Flow")
            s, options = recom_replyAr.recommender.handle_exam_recommendation(message, user_id)
            print(f"[DEBUG] Updated prev_data after response: {storage.get_prev_data(user_id)}")
            if not options:
                storage.clear_data(user_id)
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
                    storage.set_current_task(user_id, "ExamRecom")
                    s, options = recom_replyAr.recommender.handle_exam_recommendation("", user_id)
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