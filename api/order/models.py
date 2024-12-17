import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel

class Order(SQLModel, table=True):
    __tablename__ = "orders"

    order_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    start_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    end_date: datetime = Field()
    customer_id: int = Field(foreign_key="customer.customer_id")
    book_id: int = Field(foreign_key="book.book_id")
    employee_id: int = Field(foreign_key="employee.employee_id")