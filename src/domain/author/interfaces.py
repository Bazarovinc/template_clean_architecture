import abc
import uuid

from common.repositories import IBaseRepository, IRetrieveMixin

from src.domain.author.dto.author import AuthorOutSchema
from src.domain.author.dto.filter_schema import AuthorFilterSchema


class IAuthorRepository(IBaseRepository[AuthorFilterSchema], IRetrieveMixin[AuthorOutSchema]):
    pass


class IGetAuthor(abc.ABC):
    def __init__(self, repo: IAuthorRepository):
        self.repo = repo

    @abc.abstractmethod
    async def __call__(self, object_id: uuid.UUID) -> AuthorOutSchema:
        ...
