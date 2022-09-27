from dependency_injector import containers, providers

from src.domain.author.use_cases import GetAuthor
from src.domain.book.use_cases import (
    BookDeleted,
    BookUpdated,
    CreateBook,
    DeleteBook,
    GetBook,
    ListBooks,
    UpdateBook,
)


class UseCasesContainer(containers.DeclarativeContainer):
    repos = providers.DependenciesContainer()

    list_books = providers.Factory(ListBooks, repo=repos.book)
    get_book = providers.Factory(GetBook, repo=repos.book)
    create_book = providers.Factory(
        CreateBook,
        repo=repos.book,
        event_repo=repos.book_event,
        internal_event_repo=repos.book_internal_event,
    )
    update_book = providers.Factory(
        UpdateBook, repo=repos.book, get_book=get_book, event_repo=repos.book_event
    )
    delete_book = providers.Factory(
        DeleteBook, repo=repos.book, get_book=get_book, event_repo=repos.book_event
    )

    book_updated = providers.Factory(BookUpdated, repo=repos.book)
    book_deleted = providers.Factory(BookDeleted, repo=repos.book)

    get_author = providers.Factory(GetAuthor, repo=repos.author)
