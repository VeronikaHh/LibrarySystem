import uvicorn
from fastapi import FastAPI

from app.api.book.router import router as book_router
from app.api.customer.router import router as customer_router
from app.api.employee.router import router as employee_router
from app.api.order.router import router as order_router
from app.exception_handler import init_exception_handlers
from app.logger_config import logger

app = FastAPI()

app.include_router(book_router)
app.include_router(customer_router)
app.include_router(employee_router)
app.include_router(order_router)
init_exception_handlers(app)

if __name__ == "__main__":
    logger.debug("Starting app")
    uvicorn.run(app, host="0.0.0.0", port=8000)
