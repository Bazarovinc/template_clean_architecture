from common.dto import OrmModel
from common.filters.schemas import NumberFilterSpecsSchema
from pydantic import BaseModel


class BookFilterSchema(OrmModel):
    id: int | None
    ids: list[int] | None
    pagination: tuple[int, int] | None
    release_year: int | None
    name_search: str | None


class BookSpecsSchema(BaseModel):
    release_year: NumberFilterSpecsSchema


class BookFacetsSchema(BaseModel):
    release_year: NumberFilterSpecsSchema
