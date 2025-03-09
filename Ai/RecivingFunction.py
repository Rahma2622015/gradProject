from Ai.ReplyModule import ReplyModule
from Ai.TaskProcessor import TaskProcessor
from Data.dataStorage import DataStorage
from Ai.Tokeniztion import Tokenizers
from Ai.Preprocessing import Preprocessors
from Ai.TaskMapping import TaskMapper

def receive(message: str, storage: DataStorage) -> str:
    mapper = TaskMapper(r"F:\gradProject\Ai\map.json")
    reply = ReplyModule(r"F:\gradProject\Ai\response.json")
    proces=TaskProcessor()
    t=Tokenizers()
    p=Preprocessors()


    l= p.lowercase(message)
    tokens = t.tokenize(l)
    pos = t.pos_tag(tokens)
    tokens  = p.preprocess(tokens, pos)
    tasks=mapper.mapToken(tokens,pos)
    print(f"[DEBUG] Identified Tasks before processing: {tasks}")  # Add this
    pre = proces.process(tasks, storage)
    print(f"Task identified: {tasks}")  # تحقق من المهام التي تم التعرف عليها
    print(f"Processed Task Output: {pre}")  # تحقق من نتيجة TaskProcessor
    s=reply.generate_response(pre)
    return s
