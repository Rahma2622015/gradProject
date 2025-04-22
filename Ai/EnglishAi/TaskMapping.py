from Ai.EnglishAi.chattask import ChatTask
from Ai.EnglishAi.functionsForMapping import functions
from Ai.EnglishAi.max_match import match

m=match()
fun=functions()

class TaskMapper:

    def mapToken(self, tokens: list[list[str]], pos: list[list[str]]) -> list[tuple[ChatTask,]]:
        res = list()
        if not tokens or not pos or len(tokens) != len(pos):
            return [(ChatTask.UnknownTask, "Invalid input")]
        for i, data in enumerate(tokens):
            if fun.isQuestion(data):
                best_task = "UnknownTask"
                max_score = 0
                for task in m.task_definitions.keys():
                    score = m.MaxMatches(task, pos[i], data)
                    print(f"{score} : {task}")
                    if score > max_score:
                        max_score = score
                        best_task = task
                        best_task_enum = fun.convert_to_enum(best_task)
                if best_task_enum != ChatTask.UnknownTask and max_score >= 1.5:
                    res.append((best_task_enum, data,pos[i]))
                else:
                    res.append((ChatTask.UnknownTask,))
            else:
                verbIndex = fun.getPOS("VB", pos[i])
                if verbIndex != -1:
                    if data[verbIndex] == "be":
                        if pos[i][verbIndex - 1].startswith("N") and (
                                pos[i][verbIndex + 1].startswith("J") or pos[i][verbIndex + 1].startswith("N") or
                                pos[i][verbIndex + 1].endswith("N")):
                            res.append((ChatTask.StoreTask, data[verbIndex - 1], data[verbIndex + 1]))
                else:
                    res.append((ChatTask.UnknownTask,))
        if len(res) == 0:
            res.append((ChatTask.UnknownTask,))
            return res
        else:
            return res