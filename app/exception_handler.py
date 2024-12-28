from fastapi import Request
from fastapi.responses import JSONResponse

from app.api.exceptions import LibraryApiException
from .logger_config import logger


def init_exception_handlers(app):
    @app.exception_handler(LibraryApiException)
    async def library_api_exception_handler(_: Request, exc: LibraryApiException):
        detail = {"message": "api error"}
        if exc.message:
            detail["message"] = exc.message

        if exc.error_name:
            detail["message"] = f"<{exc.error_name}> - {detail['message']}"

        logger.error(exc)
        return JSONResponse(
            status_code=exc.status_code, content={"detail": detail["message"]}
        )
