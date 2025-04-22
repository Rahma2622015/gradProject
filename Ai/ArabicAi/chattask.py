from enum import Enum

class ChatTask(Enum):
    GreetingTask = 0
    ThanksTask = 1
    HelpTask = 2
    GoodbyeTask = 3
    askHelpingTask = 4
    askNameTask = 5
    CheckWellbeingTask = 6
    StoreTask = 7
    LoadTask = 8
    QuestionTask = 9
    MathTask = 10
    ConfusionTask = 11
    TypesOfProgramsTask = 12
    ExternalCoursesTask = 13
    DifficultyTask = 14
    HighGpaTask = 15
    MaterialsTypeTask = 16
    ChooseDepartmentTask = 17
    AcademicAdvisorTask = 18
    ClassificationTask = 19
    CreditHoursTask = 20
    GraduationTask = 21
    EnrollmentTask = 22
    UnknownTask = 23
    UnderstandingTask = 24
    ContradactionTask = 25
    CourseQueryTask = 26
    ProfessorQueryTask = 27
    ExamRecom=28