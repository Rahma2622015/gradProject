from Ai.TaskMapping import TaskMapper
from Ai.ReplyModule import ReplyModule
from Ai.TaskProcessor import TaskProcessor
from Data.dataStorage import DataStorage
from Ai.Tokeniztion import Tokenizers
from Ai.Preprocessing import Preprocessors

def receive(message: str, storage: DataStorage) -> str:
    mapper=TaskMapper()
    reply=ReplyModule()
    proces=TaskProcessor()
    t=Tokenizers()
    p=Preprocessors()


    l= p.lowercase(message)
    tokens = t.tokenize(l)
    pos = t.pos_tag(tokens)
    tokens  = p.preprocess(tokens, pos)
    tasks=mapper.mapToken(tokens,pos)
    pre=proces.process(tasks,storage)
    s=reply.generate_response(pre)

    return s