from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models import Book
from tests.example.factories import BookFactory


async def test_session_rollback(db_session: AsyncSession) -> None:
    obj = Book(name="test", release_year=2000)
    db_session.add(obj)
    await db_session.commit()

    assert obj

    result = await db_session.execute(select(Book).where(Book.name == "test"))
    q_obj = result.scalars().one()
    assert q_obj
    assert q_obj.id == obj.id


async def test_session_after_rollback(db_session: AsyncSession) -> None:
    result = await db_session.execute(select(func.count()).select_from(Book))
    count = result.scalar()
    assert count == 0


async def test_factory_boy(db_session: AsyncSession) -> None:
    obj = await BookFactory(name="test2")
    assert obj
    assert obj.name == "test2"

    result = await db_session.execute(select(Book).where(Book.id == obj.id))
    r_obj = result.scalars().one()
    assert r_obj.name == obj.name


async def test_factory_boy_after_rollback(db_session: AsyncSession) -> None:
    result = await db_session.execute(select(func.count()).select_from(Book))
    count = result.scalar()
    assert count == 0
