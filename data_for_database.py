from sqlalchemy.orm import Session
from Ai.EnglishAi.database import SessionLocal, Course, CourseQuestion, Answers

def add_questions_and_answers_for_courses(session: Session, short_name: str, questions_and_answers: dict):
    # استرجاع المادة بناءً على الـ short_name
    course = session.query(Course).filter(Course.short_name == short_name).first()

    if not course:
        print(f"لا يوجد مادة بالـ short_name {short_name}.")
        return

    # إضافة الأسئلة والإجابات للمادة
    for question_text, answers_dict in questions_and_answers.items():  # استخدم items() لاستخراج الأسئلة والإجابات
        # إضافة السؤال للمادة
        new_question = CourseQuestion(question=question_text, course_id=course.id)
        session.add(new_question)
        session.commit()  # تأكيد إضافة السؤال

        # إضافة الإجابات للسؤال
        for answer_text, score in answers_dict.items():  # الإجابات تكون عبارة عن dictionary
            new_answer = Answers(answer=answer_text, score=score, question_id=new_question.id)
            session.add(new_answer)

        session.commit()  # تأكيد إضافة الإجابات

    print(f"تم إضافة الأسئلة والإجابات للمادة '{course.name}'.")

# استخدام الفانكشن
with SessionLocal() as session:
    # البيانات الخاصة بالأسئلة والإجابات لكل مادة
    # بيانات جديدة لإضافتها إلى قاعدة البيانات
    data = {
        "ai": {
            "questions": {
                "do you enjoy finding and fixing security vulnerabilities in ai systems?": {
                    "yes, i enjoy it": 10,
                    "i find it challenging but interesting": 5,
                    "no, i don’t enjoy it": 0
                },
                "are you interested in ai ethics and its implications?": {
                    "yes, i find it fascinating": 10,
                    "i have some interest but not much knowledge": 5,
                    "no, i’m not interested": 0
                },
                "do you have strong machine learning skills for ai model development?": {
                    "yes, i am confident in my skills": 10,
                    "i have basic skills but need more practice": 5,
                    "no, i lack these skills": 0
                },
                "are you interested in the applications of ai in fields like healthcare and robotics?": {
                    "yes, i’m very interested": 10,
                    "i’m somewhat interested but not knowledgeable": 5,
                    "no, i’m not interested": 0
                }
            },
            "pass_threshold": 70
        },
        "parallel": {
            "questions": {
                "do you enjoy working with parallel computing and distributed systems?": {
                    "yes, i find it exciting": 10,
                    "i am interested but find it complex": 5,
                    "no, i don’t enjoy it": 0
                },
                "are you comfortable with parallel programming languages and tools like mpi or openmp?": {
                    "yes, i’m very comfortable": 10,
                    "i’m somewhat comfortable but need more practice": 5,
                    "no, i’m not comfortable at all": 0
                },
                "do you have a strong background in algorithm design and optimization for parallel systems?": {
                    "yes, i’m confident in these areas": 10,
                    "i have some knowledge but need more experience": 5,
                    "no, i don’t have a strong background": 0
                },
                "are you interested in ai applications like parallel neural networks and distributed deep learning?": {
                    "yes, i’m very interested": 10,
                    "i’m somewhat interested but not knowledgeable": 5,
                    "no, i’m not interested": 0
                }
            },
            "pass_threshold": 70
        },
        "image": {
            "questions": {
                "do you enjoy working with image data and transformations?": {
                    "yes, i find it exciting": 10,
                    "i am interested but find it complex": 5,
                    "no, i don’t enjoy it": 0
                },
                "are you comfortable with image processing libraries like opencv or pillow?": {
                    "yes, i’m very comfortable": 10,
                    "i’m somewhat comfortable but need more practice": 5,
                    "no, i’m not comfortable": 0
                },
                "do you have experience with machine learning for image classification?": {
                    "yes, i have experience": 10,
                    "i have some experience but need more practice": 5,
                    "no, i don’t have experience": 0
                },
                "are you interested in computer vision applications like object detection?": {
                    "yes, i’m very interested": 10,
                    "i’m somewhat interested but not knowledgeable": 5,
                    "no, i’m not interested": 0
                }
            },
            "pass_threshold": 70
        },
        "cyber": {
            "questions": {
                "do you enjoy learning about network security and protocols?": {
                    "yes, i find it fascinating": 10,
                    "i am interested but find it challenging": 5,
                    "no, i don’t enjoy it": 0
                },
                "are you comfortable with cryptography and encryption techniques?": {
                    "yes, i’m very comfortable": 10,
                    "i’m somewhat comfortable but need more practice": 5,
                    "no, i’m not comfortable": 0
                },
                "do you have experience in ethical hacking or penetration testing?": {
                    "yes, i have experience": 10,
                    "i have some experience but need more practice": 5,
                    "no, i don’t have experience": 0
                },
                "are you interested in learning about malware analysis?": {
                    "yes, i find it very interesting": 10,
                    "i’m somewhat interested but don’t know much": 5,
                    "no, i’m not interested": 0
                }
            },
            "pass_threshold": 70
        },
        "geometry": {
            "questions": {
                "do you enjoy solving geometric problems with algorithms?": {
                    "yes, i find it exciting": 10,
                    "i’m interested but find it complex": 5,
                    "no, i don’t enjoy it": 0
                },
                "are you comfortable with computational geometry algorithms like convex hull and voronoi diagrams?": {
                    "yes, i’m very comfortable": 10,
                    "i’m somewhat comfortable but need more practice": 5,
                    "no, i’m not comfortable": 0
                },
                "do you have experience with geometric data structures like kd-trees?": {
                    "yes, i have experience": 10,
                    "i have some experience but need more practice": 5,
                    "no, i don’t have experience": 0
                },
                "are you interested in applying computational geometry in areas like computer graphics or robotics?": {
                    "yes, i’m very interested": 10,
                    "i’m somewhat interested but not knowledgeable": 5,
                    "no, i’m not interested": 0
                }
            },
            "pass_threshold": 70
        },
        "bio": {
            "questions": {
                "do you enjoy working with biological data and genomic sequences?": {
                    "yes, i find it exciting": 10,
                    "i am interested but find it complex": 5,
                    "no, i don’t enjoy it": 0
                },
                "are you comfortable using bioinformatics tools like blast or genome browsers?": {
                    "yes, i’m very comfortable": 10,
                    "i’m somewhat comfortable but need more practice": 5,
                    "no, i’m not comfortable": 0
                },
                "do you have experience with data analysis techniques in genomics?": {
                    "yes, i have experience": 10,
                    "i have some experience but need more practice": 5,
                    "no, i don’t have experience": 0
                },
                "are you interested in applying bioinformatics in personalized medicine or drug development?": {
                    "yes, i’m very interested": 10,
                    "i’m somewhat interested but not knowledgeable": 5,
                    "no, i’m not interested": 0
                }
            },
            "pass_threshold": 70
        },
        "software": {
            "questions": {
                "do you enjoy designing and implementing software architectures?": {
                    "yes, i find it exciting": 10,
                    "i’m interested but find it challenging": 5,
                    "no, i don’t enjoy it": 0
                },
                "are you comfortable with software design patterns like singleton or factory?": {
                    "yes, i’m very comfortable": 10,
                    "i’m somewhat comfortable but need more practice": 5,
                    "no, i’m not comfortable": 0
                },
                "do you have experience with debugging and optimizing software systems?": {
                    "yes, i have experience": 10,
                    "i have some experience but need more practice": 5,
                    "no, i don’t have experience": 0
                },
                "are you interested in working with devops tools and ci/cd pipelines?": {
                    "yes, i’m very interested": 10,
                    "i’m somewhat interested but not knowledgeable": 5,
                    "no, i’m not interested": 0
                }
            },
            "pass_threshold": 70
        },
        "advanced ai": {
            "questions": {
                "do you enjoy working with deep learning and neural networks?": {
                    "yes, i find it exciting": 10,
                    "i’m interested but find it challenging": 5,
                    "no, i don’t enjoy it": 0
                },
                "are you comfortable with frameworks like tensorflow or pytorch for ai model development?": {
                    "yes, i’m very comfortable": 10,
                    "i’m somewhat comfortable but need more practice": 5,
                    "no, i’m not comfortable": 0
                },
                "do you have experience with reinforcement learning or other advanced ai techniques?": {
                    "yes, i have experience": 10,
                    "i have some experience but need more practice": 5,
                    "no, i don’t have experience": 0
                },
                "are you interested in applying ai to fields like robotics or autonomous systems?": {
                    "yes, i’m very interested": 10,
                    "i’m somewhat interested but not knowledgeable": 5,
                    "no, i’m not interested": 0
                }
            },
            "pass_threshold": 70
        },
        "data mining": {
            "questions": {
                "do you enjoy analyzing large datasets to extract meaningful insights?": {
                    "yes, i find it exciting": 10,
                    "i’m interested but find it complex": 5,
                    "no, i don’t enjoy it": 0
                },
                "are you comfortable using tools like weka or scikit-learn for data mining?": {
                    "yes, i’m very comfortable": 10,
                    "i’m somewhat comfortable but need more practice": 5,
                    "no, i’m not comfortable": 0
                },
                "do you have experience with clustering or classification techniques?": {
                    "yes, i have experience": 10,
                    "i have some experience but need more practice": 5,
                    "no, i don’t have experience": 0
                },
                "are you interested in applying data mining techniques to predictive analytics?": {
                    "yes, i’m very interested": 10,
                    "i’m somewhat interested but not knowledgeable": 5,
                    "no, i’m not interested": 0
                }
            },
            "pass_threshold": 70
        }

    }


        # إضافة الأسئلة والإجابات لكل مادة بناءً على الـ short_name
    for short_name, course_data in data.items():
        # البحث عن المادة باستخدام short_name
        course = session.query(Course).filter(Course.short_name == short_name).first()
        if course:
            add_questions_and_answers_for_courses(session, short_name, course_data["questions"])
        else:
            print(f"المادة {short_name} غير موجودة.")
