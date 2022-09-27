import uuid

from common.exceptions.repository_exceptions import NotFoundException
from common.exceptions.use_cases_exceptions import NotFoundHTTPException

from src.domain.author.dto.author import AuthorOutSchema
from src.domain.author.dto.filter_schema import AuthorFilterSchema
from src.domain.author.interfaces import IGetAuthor


class GetAuthor(IGetAuthor):
    async def __call__(self, object_id: uuid.UUID) -> AuthorOutSchema:
        try:
            return await self.repo.get_one(AuthorFilterSchema(id=object_id))
        except NotFoundException:
            raise NotFoundHTTPException
