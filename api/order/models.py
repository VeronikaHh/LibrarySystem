import uuid
from datetime import datetime, timezone, timedelta

from sqlmodel import Field, SQLModel


class OrderUpdate(SQLModel):
    end_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=90))
    is_returned: bool = Field(default=False)


class OrderCreate(OrderUpdate):
    customer_id: uuid.UUID = Field(foreign_key="customers.customer_id")
    book_id: uuid.UUID = Field(foreign_key="books.book_id")
    employee_id: uuid.UUID = Field(foreign_key="employees.employee_id")


class Order(OrderCreate, table=True):
    __tablename__ = "orders"

    order_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    start_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
