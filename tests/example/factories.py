import factory
from common.tests.async_alchemy_factory import AsyncSQLAlchemyModelFactory

from src.data.models import Book


class BookFactory(AsyncSQLAlchemyModelFactory):
    name = factory.Faker("sentence")
    release_year = 1234

    class Meta:
        model = Book
        sqlalchemy_session_persistence = "commit"
