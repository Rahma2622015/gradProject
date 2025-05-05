from enum import Enum

class ChatTask(Enum):
    StoreTask = 0
    LoadTask = 1
    UnknownTask = 2
    GreetingTask = 3
    QuestionTask = 4
    CheckWellbeingTask = 5
    MathTask = 6
    ThanksTask = 7
    HelpTask = 8
    GoodbyeTask = 9
    ConfusionTask = 10
    TypesOfProgramsTask = 11
    ExternalCoursesTask = 12
    DifficultyTask = 13
    HighGpaTask = 14
    MaterialsTypeTask = 15
    ChooseDepartmentTask = 16
    AcademicAdvisorTask = 17
    ClassificationTask = 18
    CreditHoursTask = 19
    GraduationTask = 20
    EnrollmentTask = 21
    AskHelpingTask = 22
    AskNameTask = 23
    ExamSystem = 26
    UnderstandingTask =27
    ContradictionTask = 28
    CourseSystem=29
    AssessGraduation=31
    ReasonsGraduation=32
    PreventDelays=33
    UnderstandRules=34
    ScheduleTask=35
    MultiCourseRecommendationTask = 36

    Training=39
    AdjustCreditLoad=40
    OptimizeStudyPlan=41
    LabAttendance=42
    GoodGPA=43
    SelectDepartment=44
    EnhanceCareerReadiness=45
    TransferBetweenDepartments=46
    GPARequirements = 47

    #Database tasks
    CourseQueryTask = 24
    ProfessorQueryTask = 25
    PrerequisitesTask=30
    CourseHours=37
    CourseDegrees=38
    HeadOfDepartment=48
    ProfessorOfCourse=49
    DepartmentOfCourse=50
    CourseOfProfessor=51
    CourseOfAssistant=52
    AssistantOfCourse=53
    AssistantTask=54
    PersonRoleQueryTask=55
    CourseRoleQueryTask=56
    ExamCourse=57
    ExamDoc=58
