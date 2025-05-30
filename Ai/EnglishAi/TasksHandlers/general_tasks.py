from Ai.EnglishAi.chattask import ChatTask

def handle_general_tasks(task):
    general_tasks = [
        ChatTask.CheckWellbeingTask, ChatTask.MathTask, ChatTask.QuestionTask,
        ChatTask.ThanksTask,ChatTask.GoodbyeTask,
        ChatTask.ConfusionTask, ChatTask.TypesOfProgramsTask, ChatTask.ExternalCoursesTask,
        ChatTask.DifficultyTask, ChatTask.HighGpaTask, ChatTask.MaterialsTypeTask,
        ChatTask.ChooseDepartmentTask, ChatTask.AcademicAdvisorTask, ChatTask.ClassificationTask,
        ChatTask.CreditHoursTask, ChatTask.GraduationTask, ChatTask.EnrollmentTask,
        ChatTask.AssessGraduation, ChatTask.ReasonsGraduation, ChatTask.PreventDelays,
        ChatTask.UnderstandRules, ChatTask.ScheduleTask, ChatTask.AskHelpingTask,
        ChatTask.ExamSystem, ChatTask.GPARequirements, ChatTask.Training, ChatTask.AdjustCreditLoad,
        ChatTask.MultiCourseRecommendationTask, ChatTask.OptimizeStudyPlan,
        ChatTask.LabAttendance, ChatTask.GoodGPA, ChatTask.SelectDepartment,
        ChatTask.EnhanceCareerReadiness, ChatTask.TransferBetweenDepartments,ChatTask.CourseSystem,
        ChatTask.ExamCourse, ChatTask.ExamDoc,
        ChatTask.ExclamationTask,ChatTask.NegativeTask,ChatTask.AffirmationTask,ChatTask.LikeOrLoveTask
    ]
    if task[0] in general_tasks:
        return [(task[0], "")]
    return []