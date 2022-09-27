from src.domain.book.dto.events import BaseBookEventSchema
from src.domain.book.interfaces import IBookUpdated


class BookUpdated(IBookUpdated):
    async def __call__(self, obj: BaseBookEventSchema) -> None:
        print("Got updated book", obj)
