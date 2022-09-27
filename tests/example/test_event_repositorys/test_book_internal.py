from unittest.mock import AsyncMock, MagicMock

from common import BaseAppContainer
from schema_registry.serializers.faust import Serializer

from src.domain.book.dto.events import SomeInternalEventSchema
from src.domain.book.interfaces import IBookInternalEventRepository


async def test_some_internal_event(_container: BaseAppContainer) -> None:
    send_mock = AsyncMock()
    topic_mock = MagicMock(send=send_mock)
    with _container.gateways.internal_topic.override(topic_mock):
        _container.registar.internal_registration.init()  # type: ignore
        obj = SomeInternalEventSchema(id=1)
        repo: IBookInternalEventRepository = _container.repos.book_internal_event()
        await repo.some_internal_event(obj)

    send_mock.assert_called_once()
    assert send_mock.call_args.kwargs["value"] == obj.dict()
    assert isinstance(send_mock.call_args.kwargs["value_serializer"], Serializer)
