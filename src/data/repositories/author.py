from common.admin import AdminRepo
from common.filters import Filter, FilterSet
from common.repositories import BaseRepository, RetrieveMixin

from src.data.models import Author
from src.domain.author.dto.author import AuthorInSchema, AuthorOutSchema
from src.domain.author.dto.filter_schema import AuthorFilterSchema


class AuthorFilterSet(FilterSet):
    id = Filter(Author, "id")


class AuthorRepository(RetrieveMixin[AuthorOutSchema], BaseRepository[Author, AuthorFilterSchema]):
    model = Author
    filter_set = AuthorFilterSet
    filter_schema = AuthorFilterSchema
    schema = AuthorOutSchema


class AuthorAdminRepository(AdminRepo[AuthorInSchema, AuthorInSchema, AuthorOutSchema]):
    model = Author
    schema = AuthorOutSchema
