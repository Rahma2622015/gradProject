from Ai.ArabicAi.chattask import ChatTask
from Ai.ArabicAi.functionsForTrivialTasks import func
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
                name_value = ""
                for j, word in enumerate(sentence):
                    if word == "اسم":
                        if j + 1 < len(sentence):
                            name_value = sentence[j + 1]
                        break
                    elif word in ["أنا", "انا"]:
                        if j + 1 < len(sentence) and sentence[j + 1] != "اسم":
                            name_value = sentence[j + 1]
                        elif j + 2 < len(sentence) and sentence[j + 1] == "اسم":
                            name_value = sentence[j + 2]
                        break
                res.append((ChatTask.GreetingTask, name_value))
                print(name_value, "اسمي ")
                if name_value:
                    res.append((ChatTask.StoreTask, "اسم", name_value))

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

                if best_task != ChatTask.UnknownTask or max_score >= 1:
                    res.append((best_task, sentence))
                else:
                    res.append((ChatTask.UnknownTask, ""))
            else:
                verbIndex = ma.getPOS("NOUN", pos[i])
                if verbIndex != -1:
                    if verbIndex < len(pos[i]) - 1 and pos[i][verbIndex].startswith("NOUN") and pos[i][verbIndex + 1].startswith("<NAME>"):
                        res.append((ChatTask.StoreTask, sentence[verbIndex], sentence[verbIndex + 1]))
                else:
                    res.append((ChatTask.UnknownTask,))
        print(f" المهمة النهائية المختارة: {res}")

        return res if res else [(ChatTask.UnknownTask,)]

