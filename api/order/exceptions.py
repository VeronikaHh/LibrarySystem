import uuid

from fastapi import status

from api.exceptions import LibraryApiException


class OrderException(LibraryApiException):

    def __init__(
            self,
            message: str = "Order service is unavailable",
            error_name: str | None = "OrderError",
            status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE,
    ) -> None:
        self.message = message
        self.error_name = error_name
        self.status_code = status_code
        super(LibraryApiException, self).__init__(message, error_name, status_code)


class OrderNotFoundException(OrderException):
    def __init__(
            self,
            order_id: uuid.UUID,
            message: str = "Order not found",
            status_code: int = status.HTTP_404_NOT_FOUND,
    ) -> None:
        message = f"{message}, id = [{str(order_id)}]"
        super(OrderException, self).__init__(message=message, status_code=status_code)


class InvalidOrderDataException(OrderException):
    def __init__(
            self,
            order_id: uuid.UUID,
            message: str = "Invalid order data",
            status_code: int = status.HTTP_400_BAD_REQUEST,
            error: str | None = None,
    ) -> None:
        message = f"{message}, order id = [{str(order_id)}]"
        if error:
            message = f"{message}, error = [{str(error)}]"
        super(OrderException, self).__init__(message=message, status_code=status_code)
