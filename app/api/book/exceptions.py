import uuid

from fastapi import status

from app.api.exceptions import LibraryApiException


class BookException(LibraryApiException):

    def __init__(
            self,
            message: str = "Book service is unavailable",
            error_name: str | None = "BookError",
            status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE,
    ) -> None:
        self.message = message
        self.error_name = error_name
        self.status_code = status_code
        super(LibraryApiException, self).__init__(message, error_name, status_code)


class BookNotFoundException(BookException):
    def __init__(
            self,
            book_id: uuid.UUID,
            message: str = "Book not found",
            status_code: int = status.HTTP_404_NOT_FOUND,
    ) -> None:
        message = f"{message}, id = [{str(book_id)}]"
        super(BookException, self).__init__(message=message, status_code=status_code)


class InvalidBookDataException(BookException):
    def __init__(
            self,
            book_id: uuid.UUID,
            message: str = "Invalid book data",
            status_code: int = status.HTTP_400_BAD_REQUEST,
            error: str | None = None,
    ) -> None:
        message = f"{message}, book id = [{str(book_id)}]"
        if error:
            message = f"{message}, error = [{str(error)}]"
        super(BookException, self).__init__(message=message, status_code=status_code)
