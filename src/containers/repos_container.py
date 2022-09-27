from common.database.db import Database
from dependency_injector import containers, providers

from src.data.event_repositories.book import BookEventRepository, BookInternalEventRepository
from src.data.repositories.author import AuthorAdminRepository, AuthorRepository
from src.data.repositories.book import BookAdminRepository, BookRepository


class ReposContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    gateways = providers.DependenciesContainer()

    db = providers.Singleton(Database, config.database)
    book = providers.Factory(BookRepository, session=db.provided.session)
    author = providers.Factory(AuthorRepository, session=db.provided.session)

    book_event = providers.Factory(
        BookEventRepository,
        models_registry=gateways.external_kafka_registers_facade,
        topic=gateways.external_topic,
    )
    book_internal_event = providers.Factory(
        BookInternalEventRepository,
        models_registry=gateways.internal_kafka_registers_facade,
        topic=gateways.internal_topic,
    )

    book_admin = providers.Factory(BookAdminRepository, session=db.provided.session)
    author_admin = providers.Factory(AuthorAdminRepository, session=db.provided.session)
