from Ai.EnglishAi.TaskMapping import TaskMapper
from Ai.EnglishAi.ReplyModule import ReplyModule
from Ai.EnglishAi.TaskProcessor import TaskProcessor
from Ai.EnglishAi.Tokeniztion import Tokenizers
from Ai.EnglishAi.Preprocessing import Preprocessors
from Ai.EnglishAi.AutoCorrect import AutoCorrector
from Ai.EnglishAi.MappingTrivialTasks import MappingTrivial
from Data.dataStorage import DataStorage
from Ai.Recommendation.ReplyModuleR import ReplyModuleRe
from Ai.EnglishAi.BigramModel import BigramModel
from Ai.ArabicAi.ArabicTokenizer import ArabicTokenizers
from Ai.ArabicAi.Mapping import mapping
from Ai.ArabicAi.ArabicPreprocessor import ArabicPreprocessor
from Ai.ArabicAi.ReplyModule import replyModule
from Ai.ArabicAi.TaskProcessor import taskProcessor
from Ai.EnglishAi.chattask import ChatTask
import re
import variables

mapper = TaskMapper()
trivial_mapper = MappingTrivial()
reply = ReplyModule()
proces = TaskProcessor()
t = Tokenizers()
p = Preprocessors()
a = AutoCorrector()
recom_reply = ReplyModuleRe()
bigram_model = BigramModel(variables.Bigrams)
ARmapper = mapping()
ARreply = replyModule()
ARproces = taskProcessor()
ARt = ArabicTokenizers()
ARp = ArabicPreprocessor()

def detect_language(text):
    if re.search(r'[\u0600-\u06FF]', text):
        return "Arabic"
    elif re.search(r'[A-Za-z]', text):
        return "English"
    else:
        return "Unknown"

def is_trivial_task(tokens, trivial_mapper) -> bool:
    for sentence in tokens:
        for token in sentence:
            if (trivial_mapper.isGreetingTool(token) or trivial_mapper.isGoodbyeTool(token) or
                    trivial_mapper.isThanksTool(token) or trivial_mapper.isConfusionTool(token)):
                return True
    return False

# def is_recommendation_task(tokens, pos, mapper, allowed_tasks=None) -> bool:
#     mapped_tasks = mapper.mapToken(tokens, pos)
#     if allowed_tasks is None:
#         allowed_tasks = [ChatTaskR.ExamSystem]
#     return any(task[0] in allowed_tasks for task in mapped_tasks)

def receive(message: str, storage: DataStorage, user_id: str):
    languag = detect_language(message)
    if languag == "English":
        try:
            message_lower = p.lowercase(message)
            corrected_message = a.correct_text(message_lower)
            tokens = t.tokenize(corrected_message)
            pos = t.pos_tag(tokens)
            tokens = p.preprocess(tokens, pos)
            prev_data = storage.get_prev_data(user_id)
            print(f"[DEBUG] Current task before processing: {storage.get_current_task(user_id)}")
            s, options = "", []
            if storage.get_current_task(user_id) == "ExamSystem":
                print("[DEBUG] Continuing Exam Recommendation Flow")
                s, options = recom_reply.recommender.handle_exam_recommendation(message, user_id)
                print(f"[DEBUG] Updated prev_data after response: {storage.get_prev_data(user_id)}")
                if not options:
                    storage.clear_data(user_id)
                return s, options, True

            else:
                if is_trivial_task(tokens, trivial_mapper):
                    bigram_model.sentence_probability(tokens)
                    print("[DEBUG] Mapping using TrivialMapper")
                    tasks = trivial_mapper.mapToken(tokens, pos)
                else:
                    bigram_model.sentence_probability(tokens)
                    print("[DEBUG] Mapping using TaskMapper")
                    tasks = mapper.mapToken(tokens, pos)
                print(f"[DEBUG] Identified tasks: {tasks}, type: {type(tasks)}")
                if all(task[0] == ChatTask.UnknownTask for task in tasks):
                    print("[DEBUG] No valid recommendation task found, skipping recommendation.")
                    return "I'm not sure how to answer that.", [], False
                else:
                    if any(task[0] == ChatTask.ExamSystem for task in tasks):
                        print("[DEBUG] Handling Exam Recommendation Task")
                        storage.set_current_task(user_id, "ExamSystem")
                        s, options = recom_reply.recommender.handle_exam_recommendation("", user_id)
                        print(f"[DEBUG] First question in Exam Recommendation: {s}, options: {options}")
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
            return f"Error in English processing: {str(e)}"
    elif languag == "Arabic":
        try:
            ARtokens = ARt.tokenize(message)
            ARpos = ARt.pos_tag(ARtokens)
            ARtokens = ARp.preprocess(ARtokens)
            ARtasks = ARmapper.mapToken(ARtokens, ARpos)
            ARpre = ARproces.process(ARtasks, storage)
            print(ARtokens)
            return ARreply.generate_response(ARpre),None,None
        except Exception as e:
            return f"حدث خطأ أثناء معالجة العربية: {str(e)}"

    return "Sorry, I can't recognize this language.",None,None