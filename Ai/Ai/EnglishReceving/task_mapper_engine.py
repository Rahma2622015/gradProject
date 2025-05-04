# Ai.EnglishReceving.task_mapper_engine.py

from Ai.EnglishReceving import utils

def map_tasks(tokens, pos, f, bigram_model, trivial_mapper, grammer, use_semantic_mapperfun, mapper, m):
    if utils.is_trivial_task(tokens, f):
        bigram_model.sentence_probability(tokens)
        return trivial_mapper.mapToken(tokens, pos)
    else:
        bigram_model.sentence_probability(tokens)
        grammer.is_correct(tokens)
        grammer.get_errors(tokens)

        if use_semantic_mapperfun():
            return m.mapToken(tokens, pos)
        else:
            return mapper.mapToken(tokens, pos)
