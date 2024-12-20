import uuid

from sqlmodel import Field, SQLModel


class BookUpdate(SQLModel):
    title: str = Field()
    author: str = Field()
    genre: str = Field()
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)


class Book(BookUpdate, table=True):
    __tablename__ = "books"

    book_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
