from fastapi import status


class LibraryApiException(Exception):
    def __init__(
            self,
            message: str = "Library service is unavailable",
            error_name: str = "LibraryApiException",
            status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE,
    ) -> None:
        self.message = message
        self.error_name = error_name
        self.status_code = status_code
        super().__init__(self.message, self.error_name, self.status_code)

    def __str__(self) -> str:
        return self.message + self.error_name + str(self.status_code)
