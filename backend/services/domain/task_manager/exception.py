from fastapi import status

class BaseTaskManagerException(Exception):
    status = 0
    error_message = ''

    def __init__(self, error_message=None):
        if error_message:
            self.error_message = error_message
        super().__init__(self.error_message)

class TaskWithThisNameAlreadyExistException(BaseTaskManagerException):
    status = status.HTTP_409_CONFLICT
    error_message = "Задача с таким названием уже существует"

class FailedToDeleteTaskException(BaseTaskManagerException):
    status = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_message = "Ошибка при удалении задачи"

class FailedToUpdateTaskException(BaseTaskManagerException):
    status = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_message = "Ошибка при обновлении задачи"

class AccessUserToTaskError(BaseTaskManagerException):
    status = status.HTTP_409_CONFLICT
    error_message = "Ошибка прав доступа к задаче"