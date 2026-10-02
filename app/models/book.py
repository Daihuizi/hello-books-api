from sqlalchemy.orm import Mapped, mapped_column
from ..db import db


class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]

    @classmethod
    def from_dict(cls, book_data):
        return cls(
            title=book_data["title"],
            description=book_data["description"]
        )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }