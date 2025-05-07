from Ai.EnglishAi.chattask import ChatTask
from Ai.EnglishAi.TasksHandlers.basic_tasks import handle_basic_tasks
from Ai.EnglishAi.TasksHandlers.course_tasks import handle_course_tasks
from Ai.EnglishAi.TasksHandlers.professor_tasks import handle_professor_tasks
from Ai.EnglishAi.TasksHandlers.general_tasks import handle_general_tasks
from Ai.EnglishAi.TasksHandlers.advisor_tasks import handle_advisor_tasks  # أضيفيه لو عندك
from Modules import DataStorage
from Database.Datastorage_DB import DatabaseStorage

class TaskProcessor:

    def process(self, tasks, data: DataStorage):
        D = DatabaseStorage()
        responses = []

        # Process tasks
        for task in tasks:
            task_type = task[0]

            if task_type in [ChatTask.GreetingTask, ChatTask.StoreTask, ChatTask.AskNameTask]:
                responses.extend(handle_basic_tasks(task, data))

            elif task_type in [ChatTask.CourseRoleQueryTask]:
                responses.extend(handle_course_tasks(task, D))

            elif task_type in [ChatTask.PersonRoleQueryTask]:
                responses.extend(handle_professor_tasks(task, D))

            elif task_type in [
                ChatTask.ThanksTask, ChatTask.GoodbyeTask, ChatTask.ConfusionTask,ChatTask.ClassificationTask,
                ChatTask.DifficultyTask, ChatTask.CheckWellbeingTask, ChatTask.MathTask,
                ChatTask.QuestionTask, ChatTask.AskHelpingTask, ChatTask.TypesOfProgramsTask,
                ChatTask.ExternalCoursesTask, ChatTask.HighGpaTask, ChatTask.MaterialsTypeTask,
                ChatTask.GraduationTask, ChatTask.EnrollmentTask, ChatTask.AssessGraduation,
                ChatTask.ReasonsGraduation, ChatTask.PreventDelays, ChatTask.UnderstandRules,
                ChatTask.ScheduleTask, ChatTask.ExamSystem, ChatTask.GPARequirements, ChatTask.Training,
                ChatTask.AdjustCreditLoad, ChatTask.MultiCourseRecommendationTask, ChatTask.OptimizeStudyPlan,
                ChatTask.LabAttendance, ChatTask.GoodGPA, ChatTask.SelectDepartment, ChatTask.TransferBetweenDepartments,
                ChatTask.ExamCourse,ChatTask.ExamDoc,ChatTask.CreditHoursTask,ChatTask.CourseSystem,ChatTask.EnhanceCareerReadiness,

            ]:
                responses.extend(handle_general_tasks(task))

            elif task_type in [ChatTask.AcademicAdvisorTask, ChatTask.ChooseDepartmentTask]:
                responses.extend(handle_advisor_tasks(task))

            else:
                responses.append((ChatTask.UnknownTask, ""))

        return responses
