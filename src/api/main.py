from common.exceptions.base_http_exception import BaseHTTPException
from common.fastapi_dependency_injector import DependencyInjectorFastApi
from fastapi import Request
from fastapi.responses import JSONResponse
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.api.router import include_routers
from src.containers.container import container


def create_app() -> DependencyInjectorFastApi:
    application = DependencyInjectorFastApi(
        title=container.config.app.name(),
        root_path=container.config.app.root_path(),
        debug=container.config.app.debug(),
    )
    application.add_middleware(SentryAsgiMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=container.config.app.cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(include_routers())
    application.container = container
    return application


app = create_app()


@app.on_event("startup")
async def startup_event() -> None:
    await app.container.init_resources()  # type: ignore


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await app.container.shutdown_resources()  # type: ignore


@app.exception_handler(BaseHTTPException)
async def unicorn_exception_handler(request: Request, exc: BaseHTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status,
        content={"message": exc.message},
    )
