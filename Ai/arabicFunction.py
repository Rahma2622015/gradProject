from Ai.ArabicAi.ArabicTokenizer import ArabicTokenizers
from Ai.ArabicAi.Mapping import mapping
from Ai.ArabicAi.ArabicPreprocessor import ArabicPreprocessor
from Ai.ArabicAi.ReplyModule import replyModule
from Ai.ArabicAi.TaskProcessor import taskProcessor
ARmapper = mapping()
ARreply = replyModule()
ARproces = taskProcessor()
ARt = ArabicTokenizers()
ARp = ArabicPreprocessor()

def langArabic(message, storage):
    try:
        ARtokens = ARt.tokenize(message)
        print("tokens: ",ARtokens)
        ARpos = ARt.pos_tag(ARtokens)
        print("pos: ",ARpos)
        ARtokens = ARp.preprocess(ARtokens)
        ARtasks = ARmapper.mapToken(ARtokens, ARpos)
        print("at: ",ARtasks)
        ARpre = ARproces.process(ARtasks, storage)
        return ARreply.generate_response(ARpre),None,None
    except Exception as e:
        return f"حدث خطأ أثناء معالجة العربية: {str(e)}"