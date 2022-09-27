import uuid
from typing import Optional

from common.dto.base import BaseInSchema, BaseOutSchema, BaseSchema
from pydantic.fields import Field

from src.domain.author.dto.author import AuthorOutSchema


class BookSchema(BaseSchema):
    id: Optional[int]
    name: str = Field(..., description="Название", max_length=100)
    release_year: int = Field(..., description="Год издания")


class BookInSchema(BookSchema, BaseInSchema):
    author_id: uuid.UUID | None = Field(None, description="Id автора")


class BookOutSchema(BookSchema, BaseOutSchema):
    id: int = Field(..., description="ID")
    author: AuthorOutSchema | None
