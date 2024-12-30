import uuid

from sqlmodel import Field, SQLModel


class EmployeeUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    address: str | None = None
    is_admin: bool | None = None


class EmployeeCreate(SQLModel):
    name: str = Field()
    email: str = Field()
    phone_number: str = Field()
    address: str = Field()
    is_admin: bool = Field(default=False)


class Employee(EmployeeCreate, table=True):
    __tablename__ = "employees"

    employee_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
