from Ai.ArabicAi.ArabicTokenizer import ArabicTokenizers
from Ai.ArabicAi.Mapping import mapping
from Ai.ArabicAi.ArabicPreprocessor import ArabicPreprocessor
from Ai.ArabicAi.ReplyModule import replyModule
from Ai.ArabicAi.TaskProcessor import TaskProcessor
from Ai.Recommendation.Arabic.ArabicReplyModuleRe import ArReplyModuleRe
from Ai.Recommendation.Arabic.ArabicCoursesystem import ArRecommendationSystem
from Ai.ArabicAi.SemanticTaskMapper import SemanticTaskMapperArabic
from Modules.dataStorage import DataStorage
from Database.Datastorage_DB import DatabaseStorage

# Initialization
use_semantic_armapper = True
ARmapper = mapping()
mapper = SemanticTaskMapperArabic()
ARreply = replyModule()
ARproces = TaskProcessor()
ARt = ArabicTokenizers()
ARp = ArabicPreprocessor()
recom_replyAr = ArReplyModuleRe()
data_storage = DatabaseStorage()
memory = DataStorage()
course_recommender = ArRecommendationSystem(data_storage, memory)
