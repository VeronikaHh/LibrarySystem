import uuid
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Column, String

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class EmployeeBase(SQLModel):
    name: str = Field()
    email: str = Field(unique=True)
    phone_number: str = Field(unique=True)
    address: str = Field()
    is_admin: bool = Field(default=False)

class EmployeeResponse(BaseModel):
    employee_id: uuid.UUID = Field()
    name: str = Field()
    email: str = Field(unique=True)
    phone_number: str = Field(unique=True)
    address: str = Field()
    is_admin: bool = Field(default=False)

class EmployeeCreate(EmployeeBase):
    password: str

class EmployeeUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    address: str | None = None
    is_admin: bool | None = None


class Employee(EmployeeBase, table=True):
    __tablename__ = "employees"

    employee_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(sa_column=Column(String))  # Store only the hashed version

    # Remove the plain password field from the table model
    class Config:
        exclude = {"password"}

    def set_password(self, password: str) -> None:
        """Hash and store the password"""
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Check if the provided password matches the stored hash"""
        return pwd_context.verify(password, self.hashed_password)
