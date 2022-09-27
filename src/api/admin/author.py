from common.admin import AdminRouter
from dependency_injector.wiring import Provider

from src.containers.container import Container
from src.data.models import Author
from src.domain.author.dto.author import AuthorInSchema, AuthorOutSchema


class AuthorAdminRouter(AdminRouter[AuthorInSchema, AuthorOutSchema, AuthorInSchema]):
    model = Author
    repo_provider = Provider[Container.repos.author_admin]  # type: ignore
    default_order_by = "id"
    order_by = ["id", "name"]
    create_schema = AuthorInSchema
    update_schema = AuthorInSchema
    response_schema = AuthorOutSchema
