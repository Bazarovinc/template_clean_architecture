from dataclasses import asdict, dataclass
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import parse_obj_as

from src.containers.container import Container
from src.domain.book.dto.book import BookInSchema, BookOutSchema
from src.domain.book.dto.filter_schema import BookFacetsSchema, BookFilterSchema, BookSpecsSchema
from src.domain.book.interfaces import ICreateBook, IDeleteBook, IGetBook, IListBooks, IUpdateBook

router = APIRouter()


@dataclass
class BookQuerys:
    ids: list[int] | None = Query(None)
    offset: int = Query(0)
    limit: int = Query(10)
    release_year: int | None = Query(None)
    name_search: str | None = Query(None)

    @property
    def pagination(self) -> tuple[int, int]:
        return self.offset, self.limit


@router.get("/", response_model=List[BookOutSchema])
@inject
async def get_books(
    filter_args: BookQuerys = Depends(BookQuerys),
    use_case: IListBooks = Depends(Provide[Container.use_cases.list_books]),
) -> List[BookOutSchema]:
    filter_shema = parse_obj_as(BookFilterSchema, filter_args)
    return await use_case(filter_shema)


@router.get("/specs/", response_model=BookSpecsSchema)
@inject
async def get_specs(
    filter_args: BookQuerys = Depends(BookQuerys),
    use_case: IListBooks = Depends(Provide[Container.use_cases.list_books]),
) -> BookSpecsSchema:
    filter_shema = parse_obj_as(BookFilterSchema, filter_args)
    return await use_case.specs(filter_shema)


@router.get("/facets/", response_model=BookFacetsSchema)
@inject
async def get_facets(
    filter_args: BookQuerys = Depends(BookQuerys),
    use_case: IListBooks = Depends(Provide[Container.use_cases.list_books]),
) -> BookFacetsSchema:
    filter_shema = parse_obj_as(BookFilterSchema, filter_args)
    return await use_case.facets(filter_shema)


@router.get("/{book_id}/", response_model=BookOutSchema)
@inject
async def get_book(
    book_id: int,
    use_case: IGetBook = Depends(Provide[Container.use_cases.get_book]),
) -> BookOutSchema:
    return await use_case(book_id)


@router.post(
    "/",
    response_model=BookOutSchema,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_book(
    new_book: BookInSchema,
    use_case: ICreateBook = Depends(Provide[Container.use_cases.create_book]),
) -> BookOutSchema:
    return await use_case(new_book)


@router.put(
    "/{book_id}/",
    response_model=BookOutSchema,
)
@inject
async def update_book(
    book_id: int,
    book_data: BookInSchema,
    use_case: IUpdateBook = Depends(Provide[Container.use_cases.update_book]),
) -> BookOutSchema:
    return await use_case(book_id, book_data)


@router.delete(
    "/{book_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_book(
    book_id: int,
    use_case: IDeleteBook = Depends(Provide[Container.use_cases.delete_book]),
) -> Response:
    await use_case(book_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
