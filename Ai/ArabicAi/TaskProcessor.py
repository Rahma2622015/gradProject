from Ai.ArabicAi.chattask import ChatTask
from Ai.ArabicAi.TasksHandlers.basic_tasks import handle_basic_tasks
from Ai.ArabicAi.TasksHandlers.course_tasks import handle_course_tasks
from Ai.ArabicAi.TasksHandlers.professor_tasks import handle_professor_tasks
from Ai.ArabicAi.TasksHandlers.general_tasks import handle_general_tasks
from Modules.dataStorage import DataStorage
from Database.Datastorage_DB import DatabaseStorage

class TaskProcessor:

    def process(self, tasks, data: DataStorage):
        D = DatabaseStorage()
        responses = []
        name_from_greeting = None
        skip_store_response = False

        # Handle GreetingTask
        for task in tasks:
            if task[0] == ChatTask.GreetingTask and task[1]:
                name_from_greeting = task[1]

        # Handle StoreTask
        for task in tasks:
            if task[0] == ChatTask.StoreTask and task[1] == "اسم" and task[2] == name_from_greeting:
                skip_store_response = True

        # Process tasks
        for task in tasks:

            task_type = task[0]

            if task_type in [ChatTask.GreetingTask, ChatTask.StoreTask, ChatTask.askNameTask]:
                responses.extend(handle_basic_tasks(task, data, skip_store_response, name_from_greeting))

            elif task_type in [ChatTask.CourseRoleQueryTask]:
                responses.extend(handle_course_tasks(task,D))

            elif task_type in [ChatTask.PersonRoleQueryTask]:
                responses.extend(handle_professor_tasks(task,D))

            elif task_type in [
                  ChatTask.HelpTask  ,ChatTask.ThanksTask, ChatTask.GoodbyeTask, ChatTask.ConfusionTask, ChatTask.DifficultyTask,
                    ChatTask.AcademicAdvisorTask, ChatTask.ChooseDepartmentTask, ChatTask.CheckWellbeingTask,
                    ChatTask.MathTask, ChatTask.QuestionTask, ChatTask.TypesOfProgramsTask, ChatTask.ExternalCoursesTask,
                    ChatTask.HighGpaTask, ChatTask.MaterialsTypeTask, ChatTask.ClassificationTask,
                    ChatTask.CreditHoursTask, ChatTask.GraduationTask, ChatTask.EnrollmentTask,
                    ChatTask.AssessGraduation, ChatTask.ReasonsGraduation, ChatTask.PreventDelays,
                    ChatTask.UnderstandRules, ChatTask.ScheduleTask, ChatTask.GPARequirements, ChatTask.Training,
                    ChatTask.AdjustCreditLoad, ChatTask.MultiCourseRecommendationTask, ChatTask.OptimizeStudyPlan,
                    ChatTask.LabAttendance, ChatTask.GoodGPA, ChatTask.SelectDepartment,
                    ChatTask.EnhanceCareerReadiness, ChatTask.TransferBetweenDepartments,
                    ChatTask.ExamCourse,ChatTask.ExamDoc
                    ]:
                    responses.extend(handle_general_tasks(task))

            else:
                responses.append((ChatTask.UnknownTask, ""))

        return responses
