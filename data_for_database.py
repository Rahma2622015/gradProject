from sqlalchemy.orm import Session
from Ai.EnglishAi.database import SessionLocal, Course, CourseQuestion, Answers

courses_dict = {
    "comp102": {"name": "introduction to computers"},
    "comp104": {"name": "programming 1"},
    "comp106": {"name": "logic design"},
    "comp201": {"name": "algorithm design and analysis"},
    "comp202": {"name": "data structure"},
    "comp203": {"name": "theory of computation"},
    "comp204": {"name": "computer network"},
    "comp205": {"name": "object oriented programming "},
    "comp206": {"name": "web programming"},
    "comp207": {"name": "database system"},
    "comp208": {"name": "automata theory"},
    "comp210": {"name": "graph algorithm"},
    "comp301": {"name": "advanced programming"},
    "comp302": {"name": "algorithm implementation"},
    "comp303": {"name": "programming semantics"},
    "comp304": {"name": "compiler design"},
    "comp305": {"name": "computational complexity"},
    "comp306": {"name": "computer graphics"},
    "comp307": {"name": "operating system"},
    "comp308": {"name": "cryptography"},
    "comp309": {"name": "multimedia systems"},
    "comp310": {"name": "advanced wed programming"},
    "comp314": {"name": "advanced database"},
    "comp401": {"name": "artificial intelligence"},
    "comp402": {"name": "bioinformatics"},
    "comp403": {"name": "parallel computing"},
    "comp404": {"name": "software engineering"},
    "comp405": {"name": "computer project 1"},
    "comp407": {"name": "image processing"},
    "comp408": {"name": "advanced artificial intelligence"},
    "comp409": {"name": "cybersecurity"},
    "comp411": {"name": "computational geometry"},
    "comp416": {"name": "data mining"}
}

session = SessionLocal()

try:
    for code, data in courses_dict.items():
        name_no_space = data["name"].replace(" ", "").lower()
        course = session.query(Course).filter_by(code=code).first()
        if course:
            course.name = name_no_space
            print(f"edit course that code {code}: {data['name']} → {name_no_space}")
        else:
            print(f"not found course with {code}")

    session.commit()
    print("save susecc")

except Exception as e:
    session.rollback()
    print("error", e)

finally:
    session.close()