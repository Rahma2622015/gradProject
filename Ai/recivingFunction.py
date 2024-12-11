from Ai.TaskMapping import TaskMapper
from Ai.reply_module import ReplyModule
from Ai.taskProcessor import TaskProcessor
from Data.dataStorage import DataStorage
from Ai.Tokeniztion import Tokenizers
from Ai.NewPreprocessing import Preprocessors

def receive(message: str, storage: DataStorage) -> str:
    mapper=TaskMapper()
    reply=ReplyModule()
    proces=TaskProcessor()
    t=Tokenizers()
    p=Preprocessors()

    l= p.lowercase(message)
    #pu=preprocessor.remove_punctuation(l)

    tokens = t.tokenize(l)
    pos = t.pos_tag(tokens)
    tokens  = p.preprocess(tokens, pos)
    tasks=mapper.mapToken(tokens,pos)
    pre=proces.process(tasks,storage)
    s=reply.generate_response(pre)

    return s