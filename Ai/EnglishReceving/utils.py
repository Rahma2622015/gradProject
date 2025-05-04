def is_trivial_task(tokens, f) -> bool:
    for sentence in tokens:
        for token in sentence:
            if (f.isGreetingTool(token) or f.isGoodbyeTool(token) or
                f.isThanksTool(token) or f.isConfusionTool(token)):
                return True
    return False
