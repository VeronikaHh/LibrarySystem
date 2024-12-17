import uuid

from sqlmodel import Field, SQLModel

class Employee(SQLModel, table=True):
    __tablename__ = "employees"

    employee_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field()
    email: str = Field()
    phone_number: str = Field()
    address: str = Field()
    is_admin: bool = Field(default=False)