from Ai.chattask import ChatTask

class TaskDefinitions:
    def __init__(self):
        self.task_definitions = {
            ChatTask.CheckWellbeingTask: {
                "QuestionKeywords": ["how", "what"],
                "VerbKeywords": ["be"],
                "SubjectKeywords": ["you"],
                "ObjectKeywords": ["feel", "do", "health", "mood", "up", "day"]
            },
            ChatTask.MathTask: {
                "QuestionKeywords": ["do","how","be"],
                "VerbKeywords": ["be", "should", "could", "need","have to","require","affect"],
                "SubjectKeywords": ["i", "we","me"],
                "ObjectKeywords": ["if", "math"," mathematics" ,"weak", "good"," weakness","high","school"]
            },
            ChatTask.TypesOfProgramsTask:{
            "QuestionKeywords": ["what","which"],
            "VerbKeywords": ["be","have","exist"],
            "SubjectKeywords": ["we"],
            "ObjectKeywords": ["programes", "available", "department", "math", "mathematics", "branches","collage"]
        },
            ChatTask.ExternalCoursesTask:{
                "QuestionKeywords": ["when","which","be"],
                "VerbKeywords": ["be","suppose","advise","take","should","prefer"],
                "SubjectKeywords": ["you","i","we"],
                "ObjectKeywords": ["there", "external","courses", "specific","year","certain"]
            },
            ChatTask.DifficultyTask:{
                 "QuestionKeywords": ["be", "do"],
                 "VerbKeywords": ["study","think","be", "find", "seem", "perceive"],
                 "SubjectKeywords": ["you","students", "people", "we", "they"],
                 "ObjectKeywords": ["subjects","more","cs","computer science","difficult", "field", "major", "program","mathematics","academic","disciplines"]
            },
           ChatTask.HighGpaTask:{
               "QuestionKeywords": ["will", "be", "can", "how"],
               "VerbKeywords": ["be", "achieve", "get", "help", "receive"],
               "SubjectKeywords": ["i", "me", "students", "one"],
               "ObjectKeywords": ["GPA", "high", "gpa","good", "computer", "computer science","program","cs"]
           },
            ChatTask.MaterialsTypeTask:{
             "QuestionKeywords": ["what", "which"],
             "VerbKeywords": ["be", "use", "consist","have","will","study"],
            "SubjectKeywords": ["it", "sources", "professor","we"],
            "ObjectKeywords": ["material", "sources", "type", "content","study"]
            },
            ChatTask.chooseDepartment: {
                "QuestionKeywords": ["how", "do", "what"],
                "VerbKeywords": ["can", "have", "know", "be", "should"],
                "SubjectKeywords": ["i", "we", "factors", "criteria"],
                "ObjectKeywords": ["determine", "best", "program", "join", "among",
                                   "six", "between", "choose", "way", "decide", "most",
                                   "suitable", "consider", "select", "which", "pick",
                                   "make", "informed", "decision"]

            },
            ChatTask.academingtask: {
                "QuestionKeywords": ["what", "who", "can"],
                "VerbKeywords": ["be", "tell", "responsible", "take", "let", "provide", "act"],
                "SubjectKeywords": ["we", "you"],
                "ObjectKeywords": ["me", "meant", "academic", "advisor", "function"
                    , "opinion", "serve", "meaning", "mean", "advising", "role"
                    , "charge", "guidance", "student"]
            },
            ChatTask.classification: {
                "QuestionKeywords": ["what", "be", "can", "do", "when"],
                "VerbKeywords": ["exist", "possible", "provide", "offer"],
                "SubjectKeywords": ["college", "students", "year", "any"],
                "ObjectKeywords": ["possible", "students", "focus", "one", "field"
                    , "feasible", "topic", "artificial", "only",
                                   "intelligence", "cybersecurity", "area", "particular",
                                   "special", "major", "classification", "ai", "specialization",
                                   "start", "year", "introduce", "available", "college", "certain"
                    , "options", "stage"]
            },
            ChatTask.hours: {
                "QuestionKeywords": ["how", "what", "do", "can"],
                "VerbKeywords": ["be", "many", "long", "tell"],
                "SubjectKeywords": ["hours", "hour", "credit", "duration", "study", "you"],
                "ObjectKeywords": ["program", "credit", "computer", "science", "cs",
                                   "consist", "overall", "enroll", "studying", "allotted",
                                   "minimum", "number", "single", "me", "required", "single",
                                   "duration", "total", "include", "term", "workload"]
            },
            ChatTask.graduate: {
                "QuestionKeywords": ["how", "what", "do", "be"],
                "VerbKeywords": ["will", "take", "can", "complete", "many"],
                "SubjectKeywords": ["years", "time", "it"],
                "ObjectKeywords": ["finish", "single", "special", "cs", "program"
                    , "curriculum", "entirely", "computer", "science", "alone"
                    , "complete", "graduate", "degree", "take", "complete"
                    , "focus", "computers", "require", "typically", "duration"
                    , "need", "possible", "number", "timeframe"]
            },
            ChatTask.enroll: {
                "QuestionKeywords": ["how", "what", "do"],
                "VerbKeywords": ["be","will", "take", "can", "should", "must", "many", "may"],
                "SubjectKeywords": ["years", "time", "i", "criteria"],
                "ObjectKeywords": ["determine", "subjects", "special", "cs", "program"
                    , "content", "best", "department", "register", "apply"
                    , "term", "enroll", "standards", "courses", "enroll"
                    , "choose", "based", "which", "select", "semester", "way", "take"
                    , "use", "decide", "make", "choices", "suitable"]
            }

        }


    def get_definitions(self):
        return self.task_definitions