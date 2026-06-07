from dishka import AsyncContainer, make_async_container
from dishka.integrations.flask import FlaskProvider

from .config import Config
from .providers import ApiProvider, AppProvider, DBProvider


def setup_container(config: Config) -> AsyncContainer:
    providers = [
        FlaskProvider(),
        DBProvider(),
        ApiProvider(),
        AppProvider(),
    ]

    container = make_async_container(
        *providers,
        context={
            Config: config,
        },
    )

    return container
