from common.admin import AdminRepo
from common.filters import (
    Filter,
    FilterSet,
    ILikeFilter,
    InFilter,
    LimitOffsetPagination,
    NumberFilter,
)
from common.repositories import Repository
from sqlalchemy import select
from sqlalchemy.orm import subqueryload

from src.data.models import Book
from src.domain.book.dto.book import BookOutSchema
from src.domain.book.dto.book_admin import BookAdminInSchema, BookAdminOutSchema
from src.domain.book.dto.filter_schema import BookFacetsSchema, BookFilterSchema, BookSpecsSchema


class BookFilterSet(FilterSet):
    id = Filter(Book, "id")
    ids = InFilter(Book, "id")
    pagination = LimitOffsetPagination()
    release_year = NumberFilter(Book, "release_year")
    name_search = ILikeFilter(Book, "name")


class BookRepository(
    Repository[
        Book,
        BookFilterSchema,
        BookOutSchema,
        BookOutSchema,
        BookSpecsSchema,
        BookFacetsSchema,
    ]
):
    model = Book
    query = select(Book).options(subqueryload(Book.author))
    filter_set = BookFilterSet
    filter_schema = BookFilterSchema
    specs_schema = BookSpecsSchema
    facets_schema = BookFacetsSchema
    schema = BookOutSchema
    list_schema = list[BookOutSchema]


class BookAdminRepository(AdminRepo[BookAdminInSchema, BookAdminInSchema, BookAdminOutSchema]):
    model = Book
    schema = BookAdminOutSchema
