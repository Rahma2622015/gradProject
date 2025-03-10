from Ai.EnglishAi.chattask import ChatTask

class TaskDefinitions:
    def __init__(self):
        self.task_definitions = {
            ChatTask.CheckWellbeingTask: {
                "QuestionKeywords": ["how", "what"],
                "VerbKeywords": ["be"],
                "SubjectKeywords": ["you"],
                "ObjectKeywords": ["feel", "do", "health", "mood", "up", "day"]
            },
            ChatTask.askName:{
                "QuestionKeywords": ["what", "do"],
                "VerbKeywords": ["be","know"],
                "SubjectKeywords": ["you","my"],
                "ObjectKeywords": ["name"]
            },
            ChatTask.askHelping: {
                "QuestionKeywords": ["can", "could", "would"],
                "VerbKeywords": ["help", "assist", "aid", "ask"],
                "SubjectKeywords": ["you", "me"],
                "ObjectKeywords": ["with", "this", "question", "task"]
            },
            #end trivial
            ChatTask.MathTask: {
                "QuestionKeywords": ["do","how","be","will"],
                "VerbKeywords": ["be", "should", "could", "need",
                                 "have","require","affect","might"],
                "SubjectKeywords": ["i", "we","me","it","significant"],
                "ObjectKeywords": ["if", "math"," mathematics" ,"weak",
                                   "good"," weakness","high","school","me"
                                   ,"impact","strong","foundation","influence"
                                   ,"background","hinder"]
            },
            ChatTask.TypesOfProgramsTask:{
            "QuestionKeywords": ["what","which"],
            "VerbKeywords": ["be","have","exist"],
            "SubjectKeywords": ["we"],
            "ObjectKeywords": ["program", "available", "department",
                               "math", "mathematics", "branches","collage"]
        },
            ChatTask.ExternalCoursesTask:{
                "QuestionKeywords": ["when","which","what"],
                "VerbKeywords": ["be","suppose","advise","take","should","prefer"
                                 ,"would","recommend","focus","suggest","do"],
                "SubjectKeywords": ["you","i","we"],
                "ObjectKeywords": ["there", "external","courses","recommend"
                                   ,"specific","year","certain","focus","skill"
                                   ,"dedicate"]
            },
            ChatTask.DifficultyTask:{
                 "QuestionKeywords": ["be", "do","how","would"],
                 "VerbKeywords": ["study","think","be", "find","say" 
                                  "seem", "perceive"],
                 "SubjectKeywords": ["you","student", "people", "we", "they"],
                 "ObjectKeywords": ["subject","more","cs","tougher","harder",
                                    "computer","science","difficult", "field",
                                    "major","program","mathematics","disciplines"]
            },
            ChatTask.MaterialsTypeTask:{
             "QuestionKeywords": ["what", "which"],
             "VerbKeywords": ["be", "use", "consist","have","will","study"],
            "SubjectKeywords": ["it", "sources", "professor","we"],
            "ObjectKeywords": ["material", "sources", "type", "content","study",
                               "primary","resources","professors","knowledge"]
            },
            ChatTask.HighGpaTask: {
                "QuestionKeywords": ["what", "be", "can", "how"],
                "VerbKeywords": ["be", "achieve", "get", "earn", "receive","have"],
                "SubjectKeywords": ["i", "me", "student", "it"],
                "ObjectKeywords": ["GPA", "high", "gpa", "strong", "computer",
                                   "science", "program", "cs","degree","record"]
            },
            ChatTask.chooseDepartment: {
                "QuestionKeywords": ["how", "do", "what"],
                "VerbKeywords": ["can", "have", "know", "be", "should"],
                "SubjectKeywords": ["i", "we", "factor", "criteria"],
                "ObjectKeywords": ["determine", "best", "program", "join", "among",
                                   "six", "between", "choose", "way", "decide", "most",
                                   "suitable", "consider", "select", "which", "pick",
                                   "make", "informed", "decision"]
            },
            ChatTask.academingtask: {
                "QuestionKeywords": ["what", "who", "can"],
                "VerbKeywords": ["be", "tell", "responsible", "take",
                                 "let", "provide", "act"],
                "SubjectKeywords": ["we", "you"],
                "ObjectKeywords": ["me", "meant", "academic", "advisor", "function"
                    , "opinion", "serve", "meaning", "mean", "advising", "role"
                    , "charge", "guidance", "student"]
            },
            ChatTask.classification: {
                "QuestionKeywords": ["what", "be", "can", "do", "when"],
                "VerbKeywords": ["exist", "possible", "provide", "offer","be"],
                "SubjectKeywords": ["college", "students", "year", "any"],
                "ObjectKeywords": ["possible", "students", "focus", "one", "field"
                    , "feasible", "topic", "artificial", "only",
                                   "intelligence", "cybersecurity", "area",
                                   "particular","special", "major",
                                   "classification", "ai", "specialization",
                                   "start", "year", "introduce", "available",
                                   "college", "certain"
                    , "options", "stage"]
            },
            ChatTask.hours: {
                "QuestionKeywords": ["how", "what", "do", "can"],
                "VerbKeywords": ["be", "many", "long", "tell"],
                "SubjectKeywords": ["hours", "hour", "credit",
                                    "duration", "study", "you"],
                "ObjectKeywords": ["program", "credit", "computer", "science", "cs",
                                   "consist", "overall", "enroll","studying", "allotted",
                                   "minimum", "number", "single","me", "required",
                                   "single","duration","total", "include",
                                   "term", "workload"]
            },
            ChatTask.graduate: {
                "QuestionKeywords": ["how", "what", "do", "be"],
                "VerbKeywords": ["will", "take", "can", "complete", "many","be"],
                "SubjectKeywords": ["year", "time", "it"],
                "ObjectKeywords": ["finish", "single", "special", "cs", "program"
                    , "curriculum", "entirely", "computer", "science", "alone"
                    , "complete", "graduate", "degree", "take", "complete"
                    , "focus", "computers", "require", "typically", "duration"
                    , "need", "possible", "number", "timeframe","minimum"]
            },
            ChatTask.enroll: {
                "QuestionKeywords": ["how", "what", "do"],
                "VerbKeywords": ["be","will", "take", "can", "should",
                                 "must", "many", "may"],
                "SubjectKeywords": ["years", "time", "i", "criteria"],
                "ObjectKeywords": ["determine", "subjects", "special", "cs", "program"
                    , "content", "best", "department", "register", "apply"
                    , "term", "enroll", "standards", "courses", "enroll"
                    , "choose", "based", "which", "select", "semester", "way", "take"
                    , "use", "decide", "make", "choices", "suitable"]
            },


        }


    def get_definitions(self):
        return self.task_definitions