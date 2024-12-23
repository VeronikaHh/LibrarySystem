import uuid

from sqlmodel import Field, SQLModel


class CustomerCreateUpdate(SQLModel):
    name: str = Field()
    email: str = Field()
    phone_number: str = Field()
    is_ower: bool = Field(default=False)


class Customer(CustomerCreateUpdate, table=True):
    __tablename__ = "customers"

    customer_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
