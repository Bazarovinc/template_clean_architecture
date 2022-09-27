from common.kafka.registers import RegistryRow, register_rows
from dependency_injector import containers, providers

from src.adapters.book import BookDeletedAdapter
from src.domain.book.dto.events import (
    BookCreatedEventSchema,
    BookDeletedEventSchema,
    BookUpdatedEventSchema,
    SomeInternalEventSchema,
)


class RegistarContainer(containers.DeclarativeContainer):
    use_cases = providers.DependenciesContainer()
    gateways = providers.DependenciesContainer()

    external_registration = providers.Resource(
        register_rows,
        kafka_registers_facade=gateways.external_kafka_registers_facade,
        rows=providers.List(
            RegistryRow(
                topic="example",
                value_model=BookCreatedEventSchema,
                use_case=print,
            ),
            providers.Factory(
                RegistryRow,
                topic=gateways.external_topic,
                value_model=BookUpdatedEventSchema,
                use_case=use_cases.provided.book_updated,
            ),
            providers.Factory(
                RegistryRow,
                topic=gateways.external_topic,
                value_model=BookDeletedEventSchema,
                use_case=providers.Factory(BookDeletedAdapter, use_cases.book_deleted).provider,
            ),
        ),
    )

    internal_registration = providers.Resource(
        register_rows,
        kafka_registers_facade=gateways.internal_kafka_registers_facade,
        rows=providers.List(
            providers.Factory(
                RegistryRow,
                topic=gateways.internal_topic,
                value_model=SomeInternalEventSchema,
                use_case=use_cases.provided.book_updated,
            ),
        ),
    )
