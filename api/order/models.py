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
    customer_id: uuid.UUID = Field(foreign_key="customers.customer_id")
    book_id: uuid.UUID = Field(foreign_key="books.book_id")
    employee_id: uuid.UUID = Field(foreign_key="employees.employee_id")