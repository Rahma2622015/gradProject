from Ai.EnglishAi.TaskMapping import TaskMapper
from Ai.EnglishAi.ReplyModule import ReplyModule
from Ai.EnglishAi.TaskProcessor import TaskProcessor
from Ai.EnglishAi.Tokeniztion import Tokenizers
from Ai.EnglishAi.Preprocessing import Preprocessors
from Ai.EnglishAi.AutoCorrect import AutoCorrector
from Ai.EnglishAi.MappingTrivialTasks import MappingTrivial
from Ai.Recommendation.English.ReplyModuleR import ReplyModuleRe
from Ai.EnglishAi.bigram_model import BigramModel
from Ai.EnglishAi.chattask import ChatTask
from Modules.dataStorage import DataStorage
from Database.Datastorage_DB import DatabaseStorage
from Ai.Recommendation.English.RecomCourseSystem import RecommendationSystem
from Ai.EnglishAi.SemanticTaskMapper import SemanticTaskMapper
from Ai.EnglishAi.GrammerChecker import EnglishGrammarChecker
from Ai.EnglishAi.functionsForMapping import functions
from endPoints.ai_config_endpoints import load_ai_config
from Database.FetchDataCourses.QuestionsAndAnswers import CourseQuestionsAndAnswers
from Ai.Recommendation.English.examCourseSystem import SingleShotRecommendationSystem
from Database.FetchDataCourses.coureExamSystem import CourseSystem
from Database.FetchDataProfessors.professorExamSystem import ProfessorSystem

f=functions()
grammer=EnglishGrammarChecker()
m=SemanticTaskMapper()
mapper = TaskMapper()
trivial_mapper = MappingTrivial()
reply = ReplyModule()
proces = TaskProcessor()
t = Tokenizers()
p = Preprocessors()
a = AutoCorrector()
recom_reply = ReplyModuleRe()
bigram_model = BigramModel()
data_storage = DatabaseStorage()
memory = DataStorage()
dbs=CourseQuestionsAndAnswers()
dbcour=CourseSystem()
dbpro=ProfessorSystem()
course_recommender = RecommendationSystem(data_storage, memory,dbs)
excourse=SingleShotRecommendationSystem(data_storage, memory,dbcour,dbpro)

def is_trivial_task(tokens, f) -> bool:
    for sentence in tokens:
        for token in sentence:
            if ((f.isGreetingTool(token) or f.isGoodbyeTool(token) or
                f.isThanksTool(token) or f.isConfusionTool(token)) or f.isNegative(token)or f.isLikeOrLove(token) or f.isAffirmation(token) or f.isExclamation(token)):
                return True
    return False

def is_recommendation_complete(s: str) -> bool:
    s = s.strip().lower()
    return (
            s == "no matching exam data or professor information." or
            s.startswith("First of all, I would like to tell you that the subject is") or
            s == "sorry the answer not matched with my data " or
            s == "sorry, i couldn't find any questions for this course." or
            s == "error retrieving question data." or
            s == "Sorry, I couldn't find an exam system for the course" or
            s == "no current course data found." or
            s.startswith("based on your answers") or
            s == "no exam data available for this subject." or
            s == "no professor data available for this subject." or
            s.startswith("Sorry, I couldn't find an exam system for Dr.") or
            s == "Sorry, I couldn't identify the course or professor name from your message." or
            s.startswith("First of all, I am proud that you have reached") or
            s.startswith("firstly I would like to tell you not to worry")

    )


def config():
        return load_ai_config()

def use_semantic_mapperfun():
    return config().get("use_semantic_mapper", True)

def show_grammar_feedback_enabled():
    return config().get("show_grammar_feedback", True)

def langEnglish(message, storage):
    global g1
    try:
        message_lower = p.lowercase(message)
        corrected_message = a.correct_text(message_lower)
        tokens = t.tokenize(corrected_message)
        pos = t.pos_tag(tokens)
        if not use_semantic_mapperfun():
         tokens = p.preprocess(tokens, pos)
        prev_data = storage.get_prev_data()
        s, options = "", []
        current_task = storage.get_current_task()

        # ---------------------- Exam Recommendation System ----------------------
        if current_task == "ExamSystem":
            #print("[DEBUG] Continuing Exam Recommendation Flow")
            s, options = recom_reply.recommender.handle_exam_recommendation(message)
            if is_recommendation_complete(s):
                if not options:
                    storage.clear_data()
                    storage.set_current_task(None)
                    return s, options, False
            return s, options, True

        # ---------------------- Course Recommendation System ----------------------
        elif current_task == "CourseSystem":
            s, options = course_recommender.receive_answer(message.strip())
            if is_recommendation_complete(s):
                storage.clear_data()
                storage.set_current_task(None)
                return s, options, False
            if not options:
                storage.clear_data()
            return s, options, True

        # ---------------------- Multi-Course Recommendation System ----------------------
        elif current_task == "MultiCourseSystem":
            if not prev_data.get("all_courses"):
                course_names = t.extract_all_course_names(message)
                if course_names:
                    response, options = recom_reply.course_selection_recommender.start({
                        "message": message_lower,
                        "courses": course_names
                    })
                    s = response if isinstance(response, str) else "Error processing multi-course recommendation."
                else:
                    s = "Sorry, I couldn't detect the course names from your question."
            else:
                s, options = recom_reply.course_selection_recommender.handle_answer(message)

            if is_recommendation_complete(s):
                storage.clear_data()
                storage.set_current_task(None)
                return s, options, False
            else:
                return s, options, True


        # ---------------------- Start New Task ----------------------
        else:
            if is_trivial_task(tokens, f):
                tasks = trivial_mapper.mapToken(tokens, pos)
                g1, g2 = [True], []
            else:

                if use_semantic_mapperfun():
                    g1 = grammer.is_correct(tokens)
                    g2 = grammer.get_errors(tokens)
                    print(" Mapping using SemanticTaskMapper")
                    tasks = m.mapToken(tokens, pos)
                else:
                    bigram_results = bigram_model.sentence_probability(tokens)
                    if any(result[0] == "UnknownTask" for result in bigram_results):
                        print(" Result: UnknownTask (at least one bigram is zero)")
                        return "Oh dear, I think I missed something there! Would you mind explaining it differently? I'd love to get this right for you.💕.", [], False
                    g1, g2 = [True], []
                    tasks = mapper.mapToken(tokens, pos)

            if all(task[0] == ChatTask.UnknownTask for task in tasks):
                return "I might need a bit more info to get it right 🤓 Could you tell me a bit more?", [], False

            else:
                if any(task[0] == ChatTask.ExamSystem for task in tasks):
                    storage.set_current_task("ExamSystem")
                    s, options = recom_reply.recommender.handle_exam_recommendation("")
                    return s, options, True

                if any(task[0] == ChatTask.CourseSystem for task in tasks):
                    storage.set_current_task("CourseSystem")
                    course_name = t.extract_course_name(corrected_message)
                    if course_name:
                        s, options = course_recommender.start_recommendation(course_name)
                    else:
                        s = "Please mention a valid course name so I can recommend suitable subjects."
                    return s, options, True

                if any(task[0] == ChatTask.MultiCourseRecommendationTask for task in tasks):
                    storage.set_current_task("MultiCourseSystem")
                    course_names = t.extract_all_course_names(corrected_message)
                    storage.save_data("all_courses", course_names)
                    if course_names:
                        response, options = recom_reply.course_selection_recommender.start({
                            "message": corrected_message,
                            "courses": course_names
                        })
                        s = response if isinstance(response, str) else "Error processing multi-course recommendation."
                    else:
                        s = "Sorry, I couldn't detect the course names from your question."
                    return s, options, True

                if any(task[0] == ChatTask.ExamDoc for task in tasks):
                    storage.set_current_task("CourseExSystem")
                    if isinstance(s, str):
                        s, options = excourse.handle_user_message(corrected_message)
                    else:
                        s = "Please mention a valid course name so I can recommend suitable subjects."
                    storage.set_current_task(None)
                    return s, options, False

                if any(task[0] == ChatTask.ExamCourse for task in tasks):
                    storage.set_current_task("ExamDoc")
                    if isinstance(s,str):
                        s, options = excourse.handle_user_message(corrected_message)
                    else:
                        s = "Please mention a valid doctor name so I can recommend suitable subjects."
                    storage.set_current_task(None)
                    return s, options, False

            processed_tasks = proces.process(tasks, storage)
            response = reply.generate_response(processed_tasks)

            if isinstance(response, tuple):
                s, options = response if len(response) == 2 else (response[0], [])
            else:
                s, options = response, []

        if not s:
            s = "I'm sorry, I couldn't process your request."
        if not options:
            options = []

        if use_semantic_mapperfun():
            if any(g == False for g in g1):
                    flat_errors = [error for sublist in g2 for error in sublist]
                    if flat_errors and show_grammar_feedback_enabled():
                        grammar_feedback = "Here are a few grammar notes I spotted:\n- " + "\n- ".join(flat_errors)
                        comment = "I hope this helps clarify things 😊 Let me know if you meant something else!"
                        s = f"{grammar_feedback}\n\n{comment}\n\n{s}"

        return s, options, False

    except Exception as e:
        return (f"Error in English proces"
                f"+sing: {str(e)}"), [], False