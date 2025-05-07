from Ai.ArabicAi.ArabicTokenizer import ArabicTokenizers
from Ai.ArabicAi.Mapping import mapping
from Ai.ArabicAi.ArabicPreprocessor import ArabicPreprocessor
from Ai.ArabicAi.ReplyModule import replyModule
from Ai.ArabicAi.TaskProcessor import TaskProcessor
from Ai.Recommendation.Arabic.ArabicReplyModuleRe import ArReplyModuleRe
from Ai.Recommendation.Arabic.ArabicCoursesystem import ArRecommendationSystem
from Ai.ArabicAi.chattask import ChatTask
from Ai.ArabicAi.SemanticTaskMapper import SemanticTaskMapperArabic
from Modules.dataStorage import DataStorage
from Database.Datastorage_DB import DatabaseStorage
from Database.FetchDataCourses.QuestionsAndAnswers import CourseQuestionsAndAnswers
from Ai.Recommendation.Arabic.ArabExamCourseSys import ArSingleShotRecommendationSystem
from Database.FetchDataCourses.coureExamSystem import CourseAssistant
from Database.FetchDataProfessors.professorExamSystem import CourseAssistantPr
from Ai.ArabicAi.Autocorrect import ArabicSpellChecker
import variables

use_semantic_armapper=True
ARmapper = mapping()
mapper=SemanticTaskMapperArabic()
ARreply = replyModule()
ARproces = TaskProcessor()
ARt = ArabicTokenizers()
ARp = ArabicPreprocessor()
auto=ArabicSpellChecker()
recom_replyAr = ArReplyModuleRe()
data_storage = DatabaseStorage()
memory = DataStorage()
dbs=CourseQuestionsAndAnswers()
dbcour=CourseAssistant()
dbpro=CourseAssistantPr()
course_recommender = ArRecommendationSystem(data_storage, memory,dbs)
excourse=ArSingleShotRecommendationSystem(data_storage, memory,dbcour,dbpro)

def is_ar_recommendation_complete(s: str) -> bool:
    s = s.strip()
    return (
        s == "لا يوجد نظام امتحانات متاح لهذه المعلومات." or
        s.startswith("نظام الامتحانات ل") or
        s == "اسف لا يوجد اسئلة متاحة لهذا الكورس" or
        s == "لا توجد بيانات حالية عن المقرر." or
        s == "حدث خطأ أثناء معالجة إجابتك. حاول مرة أخرى." or
        s.startswith("النتيجة") or
        s == "عذرًا، لم أتمكن من العثور على أي أسئلة لهذا الكورس." or
        s == "لا توجد بيانات حالية لهذه المواد." or
        s.startswith("بناءً على إجاباتك") or
        s == "حدث خطأ أثناء جلب بيانات السؤال." or
        s== "نوع الإدخال غير صحيح. من فضلك أدخل قائمة أو جملة تحتوي على أسماء المقررات." or
        s=="عذرًا، لم أتمكن من استخراج أسماء مقررات صالحة من رسالتك." or
        s.startswith("نظام الامتحان")
    )

def langArabic(message, storage):
    try:
        corrected_message = auto.auto_correct(message)
        ARtokens = ARt.tokenize(corrected_message)
        print("tokens: ", ARtokens)
        ARpos = ARt.pos_tag(ARtokens)
        print("pos: ",ARpos)
        #if not use_semantic_armapper:
        ARtokens = ARp.preprocess(ARtokens)
        print("artokens: ",ARtokens)
        prev_data = storage.get_prev_data()

        print(f"[DEBUG] Current task before processing: {storage.get_current_task()}")
        s, options = "", []
        current_task = storage.get_current_task()

        if current_task == "ExamSystem":
            print("[DEBUG] Continuing Exam Recommendation Flow")
            s, options = recom_replyAr.recommender.handle_exam_recommendation(message)
            print(f"[DEBUG] Updated prev_data after response: {storage.get_prev_data()}")
            if is_ar_recommendation_complete(s):
                storage.clear_data()
                storage.set_current_task(None)
                return s, options, False
            if not options:
                storage.clear_data()
            return s, options, True

        elif current_task == "CourseSystem":
            print("[DEBUG] Continuing Course Recommendation Flow")
            s, options = course_recommender.receive_answer(message.strip()) if isinstance(
                course_recommender.receive_answer(message.strip()), tuple) else (
            course_recommender.receive_answer(message.strip()), [])
            if is_ar_recommendation_complete(s):
                storage.clear_data()
                storage.set_current_task(None)
                return s, options, False
            if not options:
                storage.clear_data()
            return s, options, True
        elif current_task  == "MultiCourseSystem":
            print("[DEBUG] Continuing Multi-Course Recommendation Flow")
            if not prev_data.get("all_courses"):
                course_names = ARp.extract_all_course_names(message)
                print(f"[INFO] Detected course names: {course_names}")
                if course_names:
                    response, options = recom_replyAr.course_selection_recommender.startswith(course_names)
                    s = response if isinstance(response, str) else "Error processing multi-course recommendation."
                else:
                    s = "Sorry, I couldn't detect the course names from your question."
            else:
                s, options = recom_replyAr.course_selection_recommender.handle_answer(message)
            if is_ar_recommendation_complete(s):
                storage.clear_data()
                storage.set_current_task(None)
                return s, options, False
            else:
                return s, options, True
        else:
            if not use_semantic_armapper:
                ARtasks = ARmapper.mapToken(ARtokens, ARpos)
            else:
                print("I am using it........")
                ARtasks=mapper.mapToken(ARtokens,ARpos)
            print(f"[DEBUG] Identified tasks: {ARtasks}, type: {type(ARtasks)}")

            if all(task[0] == ChatTask.UnknownTask for task in ARtasks):
                print("[DEBUG] No valid recommendation task found, skipping recommendation.")
                return "انا لست متاكد من الاجابة على ذلك.", [], False
            else:
                if any(task[0] == ChatTask.ExamRecom for task in ARtasks):
                    print("[DEBUG] Handling Exam Recommendation Task")
                    storage.set_current_task("ExamSystem")
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
                if any(task[0] == ChatTask.MultiCourseRecommendationTask for task in ARtasks):
                    print("[DEBUG] Handling Multi-Course Recommendation Task")
                    storage.set_current_task("MultiCourseSystem")
                    course_names =ARp.extract_all_course_names(corrected_message)
                    storage.save_data("all_courses", course_names)
                    print(f"[INFO] Detected course names: {course_names}")
                    if course_names:
                        response, options = recom_replyAr.course_selection_recommender.start(course_names)
                        s = response if isinstance(response, str) else "Error processing multi-course recommendation."
                    else:
                        s = "اسف انا لا استطيع تحديد اسماء المواد من رسالتك."
                    return s, options, True
                if any(task[0] == ChatTask.ExamDoc for task in ARtasks):
                    print("[DEBUG] Handling exam Doctor Recommendation Task")
                    storage.set_current_task("CourseExSystem")
                    if isinstance(s, str):
                        s, options = excourse.handle_user_message(corrected_message)
                    else:
                        s = "من فضلك شير الى اسم دكتور صحيح."
                    storage.set_current_task(None)
                    return s, options, False

                if any(task[0] == ChatTask.ExamCourse for task in ARtasks):
                    print("[DEBUG] Handling  exam course Recommendation Task")
                    storage.set_current_task("ExamDoc")
                    if isinstance(s, str):
                        s, options = excourse.handle_user_message(corrected_message)
                    else:
                        s = "من فضلك شير الى اسم مادة صحيح."
                    storage.set_current_task(None)
                    return s, options, False
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
