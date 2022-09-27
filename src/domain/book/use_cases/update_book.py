from common.exceptions.repository_exceptions import NotFoundException
from common.exceptions.use_cases_exceptions import NotFoundHTTPException

from src.domain.book.dto.book import BookInSchema, BookOutSchema
from src.domain.book.dto.events import BookUpdatedEventSchema
from src.domain.book.interfaces import IUpdateBook


class UpdateBook(IUpdateBook):
    async def __call__(self, object_id: int, updated_object: BookInSchema) -> BookOutSchema:
        # переиспользование логики получения объекта или проверки доступа актора
        # всегда можно убрать вызов другого сценария и скопировать логику в данный сценарий
        await self.get_book(object_id=object_id)

        try:
            book = await self.repo.update(object_id, updated_object.dict(exclude_unset=True))
            await self.event_repo.updated(BookUpdatedEventSchema(**book.dict()))
            return book
        except NotFoundException:
            raise NotFoundHTTPException
