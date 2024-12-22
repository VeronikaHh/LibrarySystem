import uuid

from fastapi import status

from api.exceptions import LibraryApiException


class CustomerError(LibraryApiException):

    def __init__(
            self,
            message: str = "Customer service is unavailable",
            error_name: str | None = "CustomerError",
            status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE,
    ) -> None:
        self.message = message
        self.error_name = error_name
        self.status_code = status_code
        super(LibraryApiException, self).__init__(message, error_name, status_code)


class CustomerNotFoundError(CustomerError):
    def __init__(
            self,
            customer_id: uuid.UUID,
            message: str = "Customer not found",
            status_code: int = status.HTTP_404_NOT_FOUND,
    ) -> None:
        message = f"{message}, id = [{str(customer_id)}]"
        super(CustomerError, self).__init__(message=message, status_code=status_code)


class InvalidCustomerDataError(CustomerError):
    def __init__(
            self,
            customer_id: uuid.UUID,
            message: str = "Invalid customer data",
            status_code: int = status.HTTP_400_BAD_REQUEST,
            error: str | None = None,
    ) -> None:
        message = f"{message}, customer id = [{str(customer_id)}]"
        if error:
            message = f"{message}, error = [{str(error)}]"
        super(CustomerError, self).__init__(message=message, status_code=status_code)
