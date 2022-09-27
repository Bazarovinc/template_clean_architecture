import unittest.mock
from typing import List

import pytest
from common import DependencyInjectorFastApi
from common.exceptions.use_cases_exceptions import NotFoundHTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.main import app
from src.data.models import Book
from src.domain.book.dto.book import BookInSchema
from src.domain.book.dto.filter_schema import BookFilterSchema
from src.domain.book.interfaces import ICreateBook, IDeleteBook, IGetBook, IListBooks, IUpdateBook
from tests.example.factories import BookFactory


async def test_get_all(db_session: AsyncSession) -> None:
    use_case: IListBooks = app.container.use_cases.list_books()
    books: List[Book] = await BookFactory.create_batch(3)

    service_books = await use_case(BookFilterSchema())
    assert len(service_books) == len(books)


async def test_get_by_id(db_session: AsyncSession) -> None:
    use_case: IGetBook = app.container.use_cases.get_book()
    book: Book = await BookFactory()
    service_book = await use_case(book.id)

    assert book.id == service_book.id
    assert book.name == service_book.name
    assert book.release_year == service_book.release_year


async def test_create(db_session: AsyncSession, _app: DependencyInjectorFastApi) -> None:
    test_data = {"name": "test_name", "release_year": 2000}
    obj = BookInSchema(**test_data)
    created_method_mock = unittest.mock.AsyncMock()
    event_repo_mock = unittest.mock.MagicMock(created=created_method_mock)
    some_internal_method_mock = unittest.mock.AsyncMock()
    internal_event_repo_mock = unittest.mock.MagicMock(
        some_internal_event=some_internal_method_mock
    )
    with _app.container.repos.book_event.override(event_repo_mock):
        with _app.container.repos.book_internal_event.override(internal_event_repo_mock):
            use_case: ICreateBook = app.container.use_cases.create_book()
            service_obj = await use_case(obj)

    created_method_mock.assert_called_once()
    some_internal_method_mock.assert_called_once()

    for key, value in test_data.items():
        assert getattr(service_obj, key) == value


async def test_update(db_session: AsyncSession, _app: DependencyInjectorFastApi) -> None:
    book: Book = await BookFactory()
    test_data = {"name": "test_name", "release_year": 2000}
    in_obj = BookInSchema(**test_data)
    updated_method_mock = unittest.mock.AsyncMock()
    event_repo_mock = unittest.mock.MagicMock(updated=updated_method_mock)
    with _app.container.repos.book_event.override(event_repo_mock):
        use_case: IUpdateBook = app.container.use_cases.update_book()
        service_book = await use_case(book.id, in_obj)

    updated_method_mock.assert_called_once()

    for key, value in test_data.items():
        assert getattr(service_book, key) == value


async def test_delete(db_session: AsyncSession, _app: DependencyInjectorFastApi) -> None:
    get_book: IGetBook = app.container.use_cases.get_book()
    book: Book = await BookFactory()
    deleted_method_mock = unittest.mock.AsyncMock()
    event_repo_mock = unittest.mock.MagicMock(deleted=deleted_method_mock)
    with _app.container.repos.book_event.override(event_repo_mock):
        use_case: IDeleteBook = app.container.use_cases.delete_book()
        await use_case(book.id)

    deleted_method_mock.assert_called_once()
    with pytest.raises(NotFoundHTTPException):
        await get_book(book.id)
