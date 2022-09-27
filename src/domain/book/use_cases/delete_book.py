from common.exceptions.repository_exceptions import NotFoundException
from common.exceptions.use_cases_exceptions import NotFoundHTTPException

from src.domain.book.dto.events import BookDeletedEventSchema
from src.domain.book.interfaces import IDeleteBook


class DeleteBook(IDeleteBook):
    async def __call__(self, object_id: int) -> None:
        # переиспользование логики получения объекта или проверки доступа актора
        # всегда можно убрать вызов другого сценария и скопировать логику в данный сценарий
        book = await self.get_book(object_id=object_id)

        # отлов исключения сохранён для случая, когда удаление произошло
        # в параллельной таске между проверкой и удалением в этой таске
        try:
            await self.repo.delete(object_id)
            await self.event_repo.deleted(BookDeletedEventSchema(**book.dict()))
        except NotFoundException:
            raise NotFoundHTTPException
