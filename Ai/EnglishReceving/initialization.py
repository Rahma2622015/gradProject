from Ai.EnglishAi.TaskMapping import TaskMapper
from Ai.EnglishAi.ReplyModule import ReplyModule
from Ai.EnglishAi.TaskProcessor import TaskProcessor
from Ai.EnglishAi.Tokeniztion import Tokenizers
from Ai.EnglishAi.Preprocessing import Preprocessors
from Ai.EnglishAi.AutoCorrect import AutoCorrector
from Ai.EnglishAi.MappingTrivialTasks import MappingTrivial
from Ai.Recommendation.English.ReplyModuleR import ReplyModuleRe
from Ai.EnglishAi.BigramModel import BigramModel
from Modules.dataStorage import DataStorage
from Database.Datastorage_DB import DatabaseStorage
from Ai.Recommendation.English.RecomCourseSystem import RecommendationSystem
from Ai.EnglishAi.SemanticTaskMapper import SemanticTaskMapper
from Ai.EnglishAi.GrammerChecker import EnglishGrammarChecker
from Ai.EnglishAi.functionsForMapping import functions
from endPoints.ai_config_endpoints import load_ai_config
import variables

# Initializing all components
f = functions()
grammer = EnglishGrammarChecker()
m = SemanticTaskMapper()
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


def config():
    return load_ai_config()

def use_semantic_mapperfun():
    return config().get("use_semantic_mapper", True)
