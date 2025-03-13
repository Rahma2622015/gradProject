from Ai.EnglishAi.TaskMapping import TaskMapper
from Ai.EnglishAi.ReplyModule import ReplyModule
from Ai.EnglishAi.TaskProcessor import TaskProcessor
from Data.dataStorage import DataStorage
from Ai.EnglishAi.Tokeniztion import Tokenizers
from Ai.EnglishAi.Preprocessing import Preprocessors
from Ai.EnglishAi.AutoCorrect import AutoCorrector


def receive(message: str, storage: DataStorage) -> str:
    mapper = TaskMapper()
    reply = ReplyModule()
    proces=TaskProcessor()
    t=Tokenizers()
    p=Preprocessors()
    a=AutoCorrector()


    l= p.lowercase(message)
    #auto=a.correct_text(l)
    auto=a.spell(l)
    tokens = t.tokenize(auto)
    pos = t.pos_tag(tokens)
    tokens  = p.preprocess(tokens, pos)
    tasks=mapper.mapToken(tokens,pos)
    print(f"[DEBUG] Identified Tasks before processing: {tasks}")  # Add this
    pre = proces.process(tasks, storage)
    print(f"Task identified: {tasks}")  # تحقق من المهام التي تم التعرف عليها
    print(f"Processed Task Output: {pre}")
    s=reply.generate_response(pre)
    return s
