from unittest.mock import MagicMock

from common import BaseAppContainer

from src.domain.book.dto.events import BookUpdatedEventSchema
from src.worker.app import template
from tests.example.factories import BookFactory


async def test_template_book_updated(_container: BaseAppContainer) -> None:
    book = await BookFactory()
    use_case_mock = MagicMock()
    with _container.use_cases.book_updated.override(use_case_mock):
        _container.registar.external_registration.init()  # type: ignore
        value = BookUpdatedEventSchema.from_orm(book)
        async with template.test_context() as agent:
            await agent.put(value=value)

        use_case_mock.assert_called_once_with(value)
