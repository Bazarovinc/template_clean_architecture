import uuid

from pydantic import BaseModel


class AuthorFilterSchema(BaseModel):
    id: uuid.UUID | None
