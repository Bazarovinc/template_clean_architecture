import abc
from typing import List

from common.event_repository import IEventRepository
from common.repositories import IRepository

from src.domain.book.dto.book import BookInSchema, BookOutSchema
from src.domain.book.dto.events import (
    BookCreatedEventSchema,
    BookDeletedEventSchema,
    BookUpdatedEventSchema,
    SomeInternalEventSchema,
)
from src.domain.book.dto.filter_schema import BookFacetsSchema, BookFilterSchema, BookSpecsSchema


class IBookRepository(
    IRepository[
        BookFilterSchema,
        BookOutSchema,
        BookOutSchema,
        BookSpecsSchema,
        BookFacetsSchema,
    ]
):
    pass


class IBookEventRepository(
    IEventRepository[BookCreatedEventSchema, BookUpdatedEventSchema, BookDeletedEventSchema]
):
    pass


class IBookInternalEventRepository(abc.ABC):
    @abc.abstractmethod
    async def some_internal_event(self, obj: SomeInternalEventSchema) -> None:
        ...


class IListBooks(abc.ABC):
    def __init__(self, repo: IBookRepository):
        self.repo = repo

    @abc.abstractmethod
    async def __call__(self, filter_shcema: BookFilterSchema) -> List[BookOutSchema]:
        ...

    @abc.abstractmethod
    async def specs(self, filter_shcema: BookFilterSchema) -> BookSpecsSchema:
        ...

    @abc.abstractmethod
    async def facets(self, filter_shcema: BookFilterSchema) -> BookFacetsSchema:
        ...


class IGetBook(abc.ABC):
    def __init__(self, repo: IBookRepository):
        self.repo = repo

    @abc.abstractmethod
    async def __call__(self, object_id: int) -> BookOutSchema:
        ...


class ICreateBook(abc.ABC):
    def __init__(
        self,
        repo: IBookRepository,
        event_repo: IBookEventRepository,
        internal_event_repo: IBookInternalEventRepository,
    ):
        self.repo = repo
        self.event_repo = event_repo
        self.internal_event_repo = internal_event_repo

    @abc.abstractmethod
    async def __call__(self, new_object: BookInSchema) -> BookOutSchema:
        ...


class IUpdateBook(abc.ABC):
    def __init__(self, repo: IBookRepository, get_book: IGetBook, event_repo: IBookEventRepository):
        self.repo = repo
        self.get_book = get_book
        self.event_repo = event_repo

    @abc.abstractmethod
    async def __call__(self, object_id: int, updated_object: BookInSchema) -> BookOutSchema:
        ...


class IDeleteBook(abc.ABC):
    def __init__(self, repo: IBookRepository, get_book: IGetBook, event_repo: IBookEventRepository):
        self.repo = repo
        self.get_book = get_book
        self.event_repo = event_repo

    @abc.abstractmethod
    async def __call__(self, object_id: int) -> None:
        ...


class IBookUpdated(abc.ABC):
    def __init__(self, repo: IBookRepository):
        self.repo = repo

    @abc.abstractmethod
    async def __call__(self, obj: BookUpdatedEventSchema) -> None:
        ...


class IBookDeleted(abc.ABC):
    def __init__(self, repo: IBookRepository):
        self.repo = repo

    @abc.abstractmethod
    async def __call__(self, object_id: int) -> None:
        ...
