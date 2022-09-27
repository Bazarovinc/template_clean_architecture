from common.event_repository import BaseEventRepository, EventRepository

from src.domain.book.dto.events import SomeInternalEventSchema
from src.domain.book.interfaces import IBookEventRepository, IBookInternalEventRepository


class BookEventRepository(EventRepository, IBookEventRepository):
    pass


class BookInternalEventRepository(BaseEventRepository, IBookInternalEventRepository):
    async def some_internal_event(self, obj: SomeInternalEventSchema) -> None:
        await self.send(obj)
