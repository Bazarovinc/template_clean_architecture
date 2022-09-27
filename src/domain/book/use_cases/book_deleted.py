from src.domain.book.interfaces import IBookDeleted


class BookDeleted(IBookDeleted):
    async def __call__(self, object_id: int) -> None:
        print(f"Book({object_id}) - deleted")
