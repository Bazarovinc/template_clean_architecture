from common.fastapi_dependency_injector import BaseAppContainer
from dependency_injector import containers, providers

from src.config import Settings
from src.containers.gateways import Gateways
from src.containers.registrar import RegistarContainer
from src.containers.repos_container import ReposContainer
from src.containers.use_cases import UseCasesContainer

app_config = Settings()


class Container(BaseAppContainer):
    config = providers.Configuration(pydantic_settings=[app_config])
    wiring_config = containers.WiringConfiguration(packages=["src.api.admin", "src.api.routers"])
    gateways = providers.Container(Gateways, config=config)
    repos = providers.Container(ReposContainer, config=config, gateways=gateways)
    use_cases = providers.Container(UseCasesContainer, repos=repos)

    registar = providers.Container(RegistarContainer, use_cases=use_cases, gateways=gateways)


container = Container()
