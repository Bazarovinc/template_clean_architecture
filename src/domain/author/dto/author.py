import datetime
import uuid

from common.dto import BaseInSchema, BaseOutSchema, BaseSchema
from pydantic import Field


class AuthorSchema(BaseSchema):
    id: uuid.UUID | None
    name: str = Field(..., description="ФИО")
    date_of_birth: datetime.date = Field(..., description="Дата рождения")


class AuthorInSchema(AuthorSchema, BaseInSchema):
    pass


class AuthorOutSchema(AuthorSchema, BaseOutSchema):
    id: uuid.UUID = Field(..., description="ID")
