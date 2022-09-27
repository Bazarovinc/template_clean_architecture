from typing import List

from src.domain.book.dto.book import BookOutSchema
from src.domain.book.dto.filter_schema import BookFacetsSchema, BookFilterSchema, BookSpecsSchema
from src.domain.book.interfaces import IListBooks


class ListBooks(IListBooks):
    async def __call__(self, filter_schema: BookFilterSchema) -> List[BookOutSchema]:
        return await self.repo.filter(filter_schema)

    async def specs(self, filter_schema: BookFilterSchema) -> BookSpecsSchema:
        return await self.repo.specs(filter_schema)

    async def facets(self, filter_schema: BookFilterSchema) -> BookFacetsSchema:
        return await self.repo.facets(filter_schema)
