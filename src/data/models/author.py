import datetime
import uuid
from typing import TYPE_CHECKING

from common.database import Base
from sqlalchemy import Column, Date, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from src.data.models import Book


class Author(Base):
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: str = Column(String, nullable=False, doc="ФИО")
    date_of_birth: datetime.date = Column(Date, nullable=False, doc="Дата рождения")

    books: list["Book"] = relationship("Book", back_populates="author", doc="Книги")
