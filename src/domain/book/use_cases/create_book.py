from src.domain.book.dto.book import BookInSchema, BookOutSchema
from src.domain.book.dto.events import BookCreatedEventSchema, SomeInternalEventSchema
from src.domain.book.interfaces import ICreateBook


class CreateBook(ICreateBook):
    async def __call__(self, new_object: BookInSchema) -> BookOutSchema:
        book = await self.repo.create(new_object.dict(exclude_unset=True))
        await self.event_repo.created(BookCreatedEventSchema(**book.dict()))
        await self.internal_event_repo.some_internal_event(SomeInternalEventSchema(id=book.id))
        return book
