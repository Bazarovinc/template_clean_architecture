from src.domain.book.dto.events import BookDeletedEventSchema
from src.domain.book.interfaces import IBookDeleted


class BookDeletedAdapter:
    def __init__(self, use_case: IBookDeleted):
        self.use_case = use_case

    async def __call__(self, obj: BookDeletedEventSchema) -> None:
        await self.use_case(obj.id)
