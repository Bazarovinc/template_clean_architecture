from common.admin import AdminRouter
from dependency_injector.wiring import Provider

from src.containers.container import Container
from src.data.models import Book
from src.domain.book.dto.book_admin import BookAdminInSchema, BookAdminOutSchema


class BookAdminRouter(AdminRouter[BookAdminInSchema, BookAdminOutSchema, BookAdminInSchema]):
    model = Book
    repo_provider = Provider[Container.repos.book_admin]  # type: ignore
    default_order_by = "id"
    order_by = ["id", "name"]
    create_schema = BookAdminInSchema
    update_schema = BookAdminInSchema
    response_schema = BookAdminOutSchema
