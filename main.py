import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.book.router import router as book_router
from api.customer.router import router as customer_router
from api.employee.router import router as employee_router
from api.exceptions import LibraryApiException
from api.order.router import router as order_router
from log_config import logger

app = FastAPI()

app.include_router(book_router)
app.include_router(customer_router)
app.include_router(employee_router)
app.include_router(order_router)


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


if __name__ == "__main__":
    logger.debug("Starting app")
    uvicorn.run(app, host="0.0.0.0", port=8000)
