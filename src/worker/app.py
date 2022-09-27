import inspect
from typing import Any, AsyncGenerator

import faust
from common.kafka.registers import KafkaRegistersFacade
from faust import StreamT

from src.containers.container import container

app: faust.App = container.gateways.faust_app()
external_registry: KafkaRegistersFacade = container.gateways.external_kafka_registers_facade()
internal_registry: KafkaRegistersFacade = container.gateways.internal_kafka_registers_facade()


template_topic = container.gateways.external_topic()
internal_topic = container.gateways.internal_topic()


@app.task  # type: ignore
async def on_started(*args: Any, **kwargs: Any) -> None:
    container.gateways.sentry.init()  # type: ignore
    container.registar.external_registration.init()  # type: ignore
    container.registar.internal_registration.init()  # type: ignore


@app.agent(template_topic)
async def template(messages: StreamT) -> AsyncGenerator:
    async for message in messages:
        use_case = external_registry.get_use_case(type(message))
        if use_case:
            result = use_case(message)
            if inspect.isawaitable(result):
                await result
        yield


@app.agent(internal_topic)
async def internal(messages: StreamT) -> AsyncGenerator:
    async for message in messages:
        use_case = internal_registry.get_use_case(type(message))
        if use_case:
            result = use_case(message)
            if inspect.isawaitable(result):
                await result
        yield
