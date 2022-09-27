from common.exceptions.repository_exceptions import NotFoundException
from common.exceptions.use_cases_exceptions import NotFoundHTTPException

from src.domain.book.dto.book import BookOutSchema
from src.domain.book.dto.filter_schema import BookFilterSchema
from src.domain.book.interfaces import IGetBook


class GetBook(IGetBook):
    async def __call__(self, object_id: int) -> BookOutSchema:
        try:
            return await self.repo.get_one(BookFilterSchema(id=object_id))
        except NotFoundException:
            raise NotFoundHTTPException
