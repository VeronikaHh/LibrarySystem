import uvicorn
from fastapi import FastAPI

from log_config import logger

from api.book.router import router as book_router
from api.customer.router import router as customer_router
from api.employee.router import router as employee_router
from api.order.router import router as order_router

app = FastAPI()

app.include_router(book_router)
app.include_router(customer_router)
app.include_router(employee_router)
app.include_router(order_router)

if __name__ == "__main__":
    logger.debug("Starting app")
    uvicorn.run(app, host="0.0.0.0", port=8000)