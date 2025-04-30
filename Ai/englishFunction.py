from Ai.EnglishAi.TaskMapping import TaskMapper
from Ai.EnglishAi.ReplyModule import ReplyModule
from Ai.EnglishAi.TaskProcessor import TaskProcessor
from Ai.EnglishAi.Tokeniztion import Tokenizers
from Ai.EnglishAi.Preprocessing import Preprocessors
from Ai.EnglishAi.AutoCorrect import AutoCorrector
from Ai.EnglishAi.MappingTrivialTasks import MappingTrivial
from Ai.Recommendation.English.ReplyModuleR import ReplyModuleRe
from Ai.EnglishAi.BigramModel import BigramModel
from Ai.EnglishAi.chattask import ChatTask
from Modules.dataStorage import DataStorage
from Database.Datastorage_DB import DatabaseStorage
from Ai.Recommendation.English.RecomCourseSystem import RecommendationSystem
from Ai.EnglishAi.SemanticTaskMapper import SemanticTaskMapper
from Ai.EnglishAi.GrammerChecker import EnglishGrammarChecker
from Ai.EnglishAi.functionsForMapping import functions
from endPoints.ai_config_endpoints import load_ai_config
import variables

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
bigram_model = BigramModel(variables.Bigrams)
data_storage = DatabaseStorage()
memory = DataStorage()
course_recommender = RecommendationSystem(data_storage, memory)


def is_trivial_task(tokens, f) -> bool:
    for sentence in tokens:
        for token in sentence:
            if (f.isGreetingTool(token) or f.isGoodbyeTool(token) or
                f.isThanksTool(token) or f.isConfusionTool(token)):
                return True
    return False
  
def config():
        return load_ai_config()

def use_semantic_mapper():
    return config().get("use_semantic_mapper", True)

def langEnglish(message, storage):
    try:
        message_lower = p.lowercase(message)
        corrected_message = a.correct_text(message_lower)
        tokens = t.tokenize(corrected_message)
        pos = t.pos_tag(tokens)
        tokens = p.preprocess(tokens, pos)

        prev_data = storage.get_prev_data()
        print(f"[DEBUG] Current task before processing: {storage.get_current_task()}")

        s, options = "", []
        current_task = storage.get_current_task()

        # ---------------------- Exam Recommendation System ----------------------
        if current_task == "ExamSystem":
            print("[DEBUG] Continuing Exam Recommendation Flow")
            s, options = recom_reply.recommender.handle_exam_recommendation(message)
            print(f"[DEBUG] Updated prev_data after response: {storage.get_prev_data()}")
            if s == "No exam data available for this subject.":
                storage.clear_data()
                return s, options, False
            if not options:
                storage.clear_data()
            return s, options, True

        # ---------------------- Course Recommendation System ----------------------
        elif current_task == "CourseSystem":
            print("[DEBUG] Continuing Course Recommendation Flow")
            s, options = course_recommender.receive_answer(message.strip())
            if s == "Sorry, I couldn't find any questions for this course.":
                storage.clear_data()
                return s, options, False
            if not options:
                storage.clear_data()
            return s, options, True

        # ---------------------- Multi-Course Recommendation System ----------------------
        elif current_task == "MultiCourseSystem":
            print("[DEBUG] Continuing Multi-Course Recommendation Flow")
            if not prev_data.get("all_courses"):
                course_names = t.extract_all_course_names(message)
                print(f"[INFO] Detected course names: {course_names}")
                if course_names:
                    response, options = recom_reply.course_selection_recommender.start(course_names)
                    s = response if isinstance(response, str) else "Error processing multi-course recommendation."
                else:
                    s = "Sorry, I couldn't detect the course names from your question."
            else:
                s, options = recom_reply.course_selection_recommender.handle_answer(message)
            return s, options, True

        # ---------------------- Start New Task ----------------------
        else:
            if is_trivial_task(tokens, f):
                bigram_model.sentence_probability(tokens)
                print("[DEBUG] Mapping using TrivialMapper")
                tasks = trivial_mapper.mapToken(tokens, pos)
            else:
                bigram_model.sentence_probability(tokens)
                grammer.is_correct(tokens)
                grammer.get_errors(tokens)
                if use_semantic_mapper():
                    print("[DEBUG] Mapping using SemanticTaskMapper")
                    tasks = m.mapToken(tokens, pos)
                else:
                    print("[DEBUG] Mapping using TaskMapper")
                    tasks = mapper.mapToken(tokens, pos)
            print(f"[DEBUG] Identified tasks: {tasks}, type: {type(tasks)}")

            if all(task[0] == ChatTask.UnknownTask for task in tasks):
                print("[DEBUG] No valid recommendation task found, skipping recommendation.")
                return "I'm not sure how to answer that.", [], False

            else:
                if any(task[0] == ChatTask.ExamSystem for task in tasks):
                    print("[DEBUG] Handling Exam Recommendation Task")
                    storage.set_current_task("ExamSystem")
                    s, options = recom_reply.recommender.handle_exam_recommendation("")
                    return s, options, True

                if any(task[0] == ChatTask.CourseSystem for task in tasks):
                    print("[DEBUG] Handling Course Recommendation Task")
                    storage.set_current_task("CourseSystem")
                    course_name = t.extract_course_name(corrected_message)
                    print("===> " + course_name)
                    if course_name:
                        s, options = course_recommender.start_recommendation(course_name)
                    else:
                        s = "Please mention a valid course name so I can recommend suitable subjects."
                    return s, options, True

                if any(task[0] == ChatTask.MultiCourseRecommendationTask for task in tasks):
                    print("[DEBUG] Handling Multi-Course Recommendation Task")
                    storage.set_current_task("MultiCourseSystem")
                    course_names = t.extract_all_course_names(corrected_message)
                    storage.save_data("all_courses", course_names)
                    print(f"[INFO] Detected course names: {course_names}")
                    if course_names:
                        response, options = recom_reply.course_selection_recommender.start(course_names)
                        s = response if isinstance(response, str) else "Error processing multi-course recommendation."
                    else:
                        s = "Sorry, I couldn't detect the course names from your question."
                    return s, options, True

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
