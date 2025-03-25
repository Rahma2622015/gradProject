from Ai.ArabicAi.chattask import ChatTask
from Ai.ArabicAi.functions import func
from Ai.ArabicAi.max_match import match

fun = func()
ma=match()

class mapping:

    def mapToken(self, tokens: list[list[str]], pos: list[list[str]]) -> list[tuple[ChatTask,]]:
        res = []
        score=0
        if not tokens or not pos or len(tokens) != len(pos):
            return [(ChatTask.UnknownTask, "Invalid input")]

        for i, sentence in enumerate(tokens):

            if any(fun.isGreetingTool(word) for word in sentence):
                res.append((ChatTask.GreetingTask, "اسم"))
            elif any(fun.isThanksTool(word) for word in sentence):
                res.append((ChatTask.ThanksTask, ""))
            elif any(fun.isGoodbyeTool(word) for word in sentence):
                res.append((ChatTask.GoodbyeTask, ""))
            elif any(fun.isConfusionTool(word) for word in sentence):
                res.append((ChatTask.ConfusionTask, ""))
            elif fun.isQuestion(sentence) :
                best_task = ChatTask.UnknownTask
                max_score = 0
                for task in ma.task_definitions.keys():
                    score = ma.MaxMatches(task, pos[i], sentence)
                    print(f"🔎 {score} : {task} ({sentence})")
                    if score > max_score:
                        max_score = score
                        best_task = ma.convert_to_enum(task)

                if best_task != ChatTask.UnknownTask or max_score >= 1.5:
                    res.append((best_task, sentence))
                else:
                    res.append((ChatTask.UnknownTask, ""))
            else:
                verbIndex = ma.getPOS("NOUN", pos[i])
                if verbIndex != -1:
                    if verbIndex < len(pos[i]) - 1 and pos[i][verbIndex].startswith("NOUN") and pos[i][verbIndex + 1].startswith("NOUN"):
                        res.append((ChatTask.StoreTask, sentence[verbIndex], sentence[verbIndex + 1]))
                        print("llll", (ChatTask.StoreTask, sentence[verbIndex], sentence[verbIndex + 1]))
                else:
                    res.append((ChatTask.UnknownTask,))
        print(f"🔍 عدد المطابقات لـ ChatTask.askHelpingTask: {score}")
        print(f"📌 المهمة النهائية المختارة: {res}")

        return res if res else [(ChatTask.UnknownTask,)]

