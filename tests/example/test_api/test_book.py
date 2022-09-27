import unittest.mock

from common import DependencyInjectorFastApi
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models import Book
from tests.example.factories import BookFactory


async def test_empty_book_list(test_client: AsyncClient) -> None:
    response = await test_client.get("/book/")
    assert response.status_code == 200
    assert response.json() == []


async def test_book_list(test_client: AsyncClient, db_session: AsyncSession) -> None:
    await BookFactory.create_batch(3)
    response = await test_client.get("/book/")
    assert response.status_code == 200
    assert len(response.json()) == 3


async def test_book_not_found(test_client: AsyncClient) -> None:
    response = await test_client.get("/book/1/")
    assert response.status_code == 404


async def test_book_detail(test_client: AsyncClient, db_session: AsyncSession) -> None:
    book: Book = await BookFactory()
    response = await test_client.get(f"/book/{book.id}/")
    assert response.status_code == 200
    data: dict = response.json()
    for key, value in data.items():
        assert getattr(book, key) == value


async def test_book_create_validation(test_client: AsyncClient, db_session: AsyncSession) -> None:
    invalid_data = {"name": None, "release_year": "adff"}
    response = await test_client.post("/book/", json=invalid_data)
    assert response.status_code == 422

    result = await db_session.execute(select(func.count()).select_from(Book))
    count = result.scalar()
    assert count == 0


async def test_book_create(
    test_client: AsyncClient, db_session: AsyncSession, _app: DependencyInjectorFastApi
) -> None:
    data = {"name": "Test book", "release_year": 2000}
    created_method_mock = unittest.mock.AsyncMock()
    event_repo_mock = unittest.mock.MagicMock(created=created_method_mock)
    some_internal_method_mock = unittest.mock.AsyncMock()
    internal_event_repo_mock = unittest.mock.MagicMock(
        some_internal_event=some_internal_method_mock
    )
    with _app.container.repos.book_event.override(event_repo_mock):
        with _app.container.repos.book_internal_event.override(internal_event_repo_mock):
            response = await test_client.post("/book/", json=data)
    assert response.status_code == 201

    response_data: dict = response.json()
    result = await db_session.execute(select(Book).where(Book.id == response_data.get("id")))
    book: Book = result.scalars().one()

    for key, value in response_data.items():
        assert getattr(book, key) == value


async def test_book_update_validation(test_client: AsyncClient, db_session: AsyncSession) -> None:
    book: Book = await BookFactory()
    invalid_data = {"name": None, "release_year": "adff"}
    response = await test_client.put(f"/book/{book.id}/", json=invalid_data)
    assert response.status_code == 422


async def test_book_update(
    test_client: AsyncClient, db_session: AsyncSession, _app: DependencyInjectorFastApi
) -> None:
    book: Book = await BookFactory()
    data = {"name": "Test book", "release_year": 2000}
    updated_method_mock = unittest.mock.AsyncMock()
    event_repo_mock = unittest.mock.MagicMock(updated=updated_method_mock)
    with _app.container.repos.book_event.override(event_repo_mock):
        response = await test_client.put(f"/book/{book.id}/", json=data)
    assert response.status_code == 200

    response_data: dict = response.json()
    result = await db_session.execute(select(Book).where(Book.id == response_data.get("id")))
    obj: Book = result.scalars().one()

    for key, value in data.items():
        assert getattr(obj, key) == value


async def test_book_delete_validation(test_client: AsyncClient) -> None:
    response = await test_client.delete("/book/1/")
    assert response.status_code == 404


async def test_book_delete(
    test_client: AsyncClient, db_session: AsyncSession, _app: DependencyInjectorFastApi
) -> None:
    book: Book = await BookFactory()
    deleted_method_mock = unittest.mock.AsyncMock()
    event_repo_mock = unittest.mock.MagicMock(deleted=deleted_method_mock)
    with _app.container.repos.book_event.override(event_repo_mock):
        response = await test_client.delete(f"/book/{book.id}/")
    assert response.status_code == 204

    result = await db_session.execute(select(Book).where(Book.id == book.id))
    obj = result.scalars().one_or_none()
    assert obj is None
