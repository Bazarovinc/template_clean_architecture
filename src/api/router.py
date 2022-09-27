from fastapi import APIRouter

from src.api.admin.author import AuthorAdminRouter
from src.api.admin.book import BookAdminRouter
from src.api.routers.author import router as author_router
from src.api.routers.book import router as book_router


def get_admin_router() -> APIRouter:
    admin_router = APIRouter()
    admin_router.include_router(BookAdminRouter(), prefix="/book")
    admin_router.include_router(AuthorAdminRouter(), prefix="/author")
    return admin_router


def include_routers() -> APIRouter:
    main_router = APIRouter()
    main_router.include_router(book_router, prefix="/book")
    main_router.include_router(author_router, prefix="/author")
    main_router.include_router(get_admin_router(), prefix="/admin")
    return main_router
