from sqlalchemy.orm import Session
from Ai.EnglishAi.database import SessionLocal, Course, CourseQuestion, Answers

courses_dict = {

    "comp202": {"name": "data structure"},
    "comp314": {"name": "advanced database"},
    "comp408": {"name": "advanced ai"},
    "comp416": {"name": "data mining"}
}

session = SessionLocal()

try:
    for code, data in courses_dict.items():
        name_no_space = data["name"].replace(" ", "").lower()
        course = session.query(Course).filter_by(code=code).first()
        if course:
            course.short_name = name_no_space
            print(f"✔ تم تعديل اسم الكورس {code}: {data['name']} → {name_no_space}")
        else:
            print(f"⚠ لم يتم العثور على كورس بكود {code}")

    session.commit()
    print("✅ تم حفظ كل التعديلات بنجاح.")

except Exception as e:
    session.rollback()
    print("❌ حدث خطأ:", e)

finally:
    session.close()