from random import choice
from Ai.EnglishAi.chattask import ChatTask

def handle_general_tasks(r, data):
    task_map = {
        ChatTask.TypesOfProgramsTask: "Programs",
        ChatTask.MathTask: "Math",
        ChatTask.ExternalCoursesTask: "ExternalCourses",
        ChatTask.DifficultyTask: "Difficulty",
        ChatTask.HighGpaTask: "HighGpa",
        ChatTask.MaterialsTypeTask: "MaterialType",
        ChatTask.ChooseDepartmentTask: "chooseDepartment",
        ChatTask.AcademicAdvisorTask: "AcademicAdvisorTask",
        ChatTask.ClassificationTask: "Classification",
        ChatTask.CreditHoursTask: "CreditHours",
        ChatTask.GraduationTask: "Graduation",
        ChatTask.EnrollmentTask: "Enrollment",
        ChatTask.AssessGraduation: "AssessGraduation",
        ChatTask.ReasonsGraduation: "ReasonsGraduation",
        ChatTask.PreventDelays: "PreventDelays",
        ChatTask.UnderstandRules: "UnderstandRules",
        ChatTask.ScheduleTask: "ScheduleTask",
        ChatTask.GPARequirements: "GPARequirements",
        ChatTask.Training: "Training",
        ChatTask.AdjustCreditLoad: "AdjustCreditLoad",
        ChatTask.OptimizeStudyPlan: "OptimizeStudyPlan",
        ChatTask.LabAttendance: "LabAttendance",
        ChatTask.GoodGPA: "GoodGPA",
        ChatTask.SelectDepartment: "SelectDepartment",
        ChatTask.EnhanceCareerReadiness: "EnhanceCareerReadiness",
        ChatTask.TransferBetweenDepartments: "TransferBetweenDepartments",
        ChatTask.MultiCourseRecommendationTask: "MultiCourseRecommendationTask",
        ChatTask.CourseSystem: "CourseSystem",
        ChatTask.ExamSystem: "ExamSystem"

    }

    key = task_map.get(r[0])
    if key:
        print(key,"----------------------")
        return choice(data.get(key, []))
    return None
