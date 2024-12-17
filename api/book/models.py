import uuid

from sqlmodel import Field, SQLModel

class Book(SQLModel, table=True):
    __tablename__ = "books"

    book_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field()
    author: str = Field()
    type: str = Field()
    price: float = Field()
    quantity: int = Field()