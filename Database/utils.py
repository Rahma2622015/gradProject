from rapidfuzz import process

def get_closest_match(user_input, db_names):
    match, score, _ = process.extractOne(user_input, db_names)
    return match if score > 80 else None

