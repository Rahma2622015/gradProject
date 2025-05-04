from enum import Enum

class ChatTask(Enum):
    GreetingTask = 0
    ThanksTask = 1
    GoodbyeTask = 2
    askHelpingTask = 3
    askNameTask = 4
    CheckWellbeingTask = 5
    StoreTask = 6
    LoadTask = 7
    QuestionTask = 8
    MathTask = 9
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
    UnknownTask = 22
    UnderstandingTask = 23
    ContradactionTask = 24
    ExamRecom=28
    AssessGraduation=29
    ReasonsGraduation=30
    PreventDelays=31
    UnderstandRules=32
    ScheduleTask=33

    Training=36
    AdjustCreditLoad=37
    OptimizeStudyPlan=38
    LabAttendance=39
    GoodGPA=40
    SelectDepartment=41
    EnhanceCareerReadiness=42
    TransferBetweenDepartments=43
    courseSystem=44
    MultiCourseRecommendationTask = 45
    GPARequirements = 46

    #Database tasks
    CourseQueryTask = 25
    ProfessorQueryTask = 26
    PrerequisiteQueryTask = 27
    CourseHours=34
    CourseDegrees=35
    AssistantTask=47
    HeadOfDepartment=48
    ProfessorOfCourse=49
    DepartmentOfCourse=50
    CourseOfProfessor=51
    CourseOfAssistant=52
    AssistantOfCourse=53
    PersonRoleQueryTask=54
    CourseRoleQueryTask=55
