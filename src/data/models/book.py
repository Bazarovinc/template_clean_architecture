import uuid

from common.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.data.models.author import Author


class Book(Base):
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False, doc="Название")
    release_year: int = Column(Integer, nullable=False, doc="Дата издания")

    author_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("author.id"))
    author: "Author" = relationship("Author", back_populates="books", doc="Автор")
