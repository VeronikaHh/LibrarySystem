import uuid

from fastapi import status

from api.exceptions import LibraryApiException


class EmployeeError(LibraryApiException):

    def __init__(
            self,
            message: str = "Employee service is unavailable",
            error_name: str | None = "EmployeeError",
            status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE,
    ) -> None:
        self.message = message
        self.error_name = error_name
        self.status_code = status_code
        super(LibraryApiException, self).__init__(message, error_name, status_code)


class EmployeeNotFoundError(EmployeeError):
    def __init__(
            self,
            employee_id: uuid.UUID,
            message: str = "Employee not found",
            status_code: int = status.HTTP_404_NOT_FOUND,
    ) -> None:
        message = f"{message}, id = [{str(employee_id)}]"
        super(EmployeeError, self).__init__(message=message, status_code=status_code)


class InvalidEmployeeDataError(EmployeeError):
    def __init__(
            self,
            employee_id: uuid.UUID,
            message: str = "Invalid employee data",
            status_code: int = status.HTTP_400_BAD_REQUEST,
            error: str | None = None,
    ) -> None:
        message = f"{message}, employee id = [{str(employee_id)}]"
        if error:
            message = f"{message}, error = [{str(error)}]"
        super(EmployeeError, self).__init__(message=message, status_code=status_code)
