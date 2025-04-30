from Ai.ArabicAi.chattask import ChatTask
from random import choice

def handle_general_reply(r, data):
    tag_map = {
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
        ChatTask.ExamRecom:"EamRecom",
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
    }

    key = tag_map.get(r[0], "Unknown")
    return choice(data.get(key, []))
