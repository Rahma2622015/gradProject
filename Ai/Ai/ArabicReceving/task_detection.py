

def detect_tasks(ARtokens, ARpos, use_semantic_armapper, ARmapper, mapper):
    if not use_semantic_armapper:
        return ARmapper.mapToken(ARtokens, ARpos)
    else:
        return mapper.mapToken(ARtokens, ARpos)
