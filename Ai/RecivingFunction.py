from Ai.EnglishAi.TaskMapping import TaskMapper
from Ai.EnglishAi.ReplyModule import ReplyModule
from Ai.EnglishAi.TaskProcessor import TaskProcessor
from Data.dataStorage import DataStorage
from Ai.EnglishAi.Tokeniztion import Tokenizers
from Ai.EnglishAi.Preprocessing import Preprocessors
from Ai.EnglishAi.AutoCorrect import AutoCorrector
from Ai.EnglishAi.MappingTrivialTasks import MappingTrivial

def is_trivial_task(tokens, trivial_mapper):
    for sentence in tokens:
        for token in sentence:
            if (trivial_mapper.isGreetingTool(token) or trivial_mapper.isGoodbyeTool(token) or
                trivial_mapper.isThanksTool(token) or trivial_mapper.isConfusionTool(token)):
                return True
    return False

def receive(message: str, storage: DataStorage) -> str:
    mapper = TaskMapper()
    trivial_mapper = MappingTrivial()
    reply = ReplyModule()
    proces = TaskProcessor()
    t = Tokenizers()
    p = Preprocessors()
    a = AutoCorrector()

    l = p.lowercase(message)
    auto = a.spell(l)
    tokens = t.tokenize(auto)
    pos = t.pos_tag(tokens)
    tokens = p.preprocess(tokens, pos)
    if is_trivial_task(tokens, trivial_mapper):
        print("[DEBUG] Mapping using TrivialMapper")
        tasks = trivial_mapper.mapToken(tokens, pos)
    else:
        print("[DEBUG] Mapping using TaskMapper")
        tasks = mapper.mapToken(tokens, pos)
    print(f"[DEBUG] Identified tasks: {tasks}, type: {type(tasks)}")
    pre = proces.process(tasks, storage)
    print(f"[DEBUG] Processed tasks output: {pre}, type: {type(pre)}")
    s = reply.generate_response(pre)
    return s
