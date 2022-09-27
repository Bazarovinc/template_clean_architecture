import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.containers.container import Container
from src.domain.author.dto.author import AuthorOutSchema
from src.domain.author.interfaces import IGetAuthor

router = APIRouter()


@router.get("/{author_id}/", response_model=AuthorOutSchema)
@inject
async def get_author(
    author_id: uuid.UUID,
    use_case: IGetAuthor = Depends(Provide[Container.use_cases.get_author]),
) -> AuthorOutSchema:
    return await use_case(author_id)
