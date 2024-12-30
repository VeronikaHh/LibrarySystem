import uuid

from sqlmodel import Field, SQLModel

class CustomerUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    is_ower: bool | None = None

class CustomerCreate(SQLModel):
    name: str = Field()
    email: str = Field(unique=True)
    phone_number: str = Field(unique=True)
    is_ower: bool = Field(default=False)


class Customer(CustomerCreate, table=True):
    __tablename__ = "customers"

    customer_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
