import faust
import pytest
from common.fastapi_dependency_injector import BaseAppContainer, DependencyInjectorFastApi
from common.tests.fixtures import *  # Необходимо для имопорта базовых фикстур

from src.api.main import app
from src.containers.container import container


@pytest.fixture()
def _app() -> DependencyInjectorFastApi:
    return app


@pytest.fixture()  # type: ignore
async def _container(_app: DependencyInjectorFastApi) -> BaseAppContainer:
    return container


@pytest.fixture(autouse=True)
async def in_memory_faust_app(_container: BaseAppContainer) -> faust.App:
    faust_app: faust.App = _container.gateways.faust_app("worker")
    faust_app.finalize()
    faust_app.conf.store = "memory://"  # type: ignore
    faust_app.flow_control.resume()
    return faust_app
