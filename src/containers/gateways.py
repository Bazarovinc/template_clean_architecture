from common.kafka.app import (
    get_faust_app_for_producer,
    get_faust_app_for_worker,
    get_schemaregistry_config,
)
from common.kafka.registers import KafkaRegistersFacade
from common.sentry import init_sentry
from dependency_injector import containers, providers
from faust import Topic
from schema_registry.client import SchemaRegistryClient


class Gateways(containers.DeclarativeContainer):
    config = providers.Configuration()

    sentry = providers.Resource(init_sentry, dsn=config.sentry.dsn, environment=config.sentry.env)

    # Kafka
    faust_app = providers.Selector(
        config.kafka.faust_app_type,
        worker=providers.Resource(get_faust_app_for_worker, config=config.kafka),
        producer=providers.Resource(get_faust_app_for_producer, config=config.kafka),
    )
    schemaregistry_client: providers.Provider[SchemaRegistryClient] = providers.Singleton(
        SchemaRegistryClient,
        providers.Callable(get_schemaregistry_config, config.kafka),
    )

    # Регистры
    external_kafka_registers_facade = providers.Singleton(
        KafkaRegistersFacade,
        schemaregistry_client=schemaregistry_client,
    )
    internal_kafka_registers_facade = providers.Singleton(
        KafkaRegistersFacade,
        schemaregistry_client=schemaregistry_client,
    )

    # Topics
    internal_topic = providers.Singleton(
        Topic,
        app=faust_app,
        topics=["example-internal"],
        schema=internal_kafka_registers_facade.provided.autodetect_schema,
    )
    external_topic = providers.Singleton(
        Topic,
        app=faust_app,
        topics=["example"],
        schema=external_kafka_registers_facade.provided.autodetect_schema,
    )
