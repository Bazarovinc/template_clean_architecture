import uuid

from common.dto.base import BaseInSchema, BaseOutSchema, BaseSchema
from pydantic.fields import Field


class BookAdminSchema(BaseSchema):
    id: int | None
    name: str = Field(..., description="Название", max_length=100)
    release_year: int = Field(..., description="Год издания")
    author_id: uuid.UUID | None = Field(None, description="Id автора")


class BookAdminInSchema(BookAdminSchema, BaseInSchema):
    pass


class BookAdminOutSchema(BookAdminSchema, BaseOutSchema):
    id: int = Field(..., description="ID")
