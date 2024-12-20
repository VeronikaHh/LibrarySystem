import uuid

from sqlmodel import Field, SQLModel

class EmployeeUpdate(SQLModel):
    name: str = Field()
    email: str = Field()
    phone_number: str = Field()
    address: str = Field()
    is_admin: bool = Field(default=False)

class Employee(EmployeeUpdate, table=True):
    __tablename__ = "employees"

    employee_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
