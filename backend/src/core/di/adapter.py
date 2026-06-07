from typing import Callable, Coroutine, Any, Optional

from flask import Flask
from dishka import AsyncContainer

from .functions import setup_flask_async_dishka, verify_dishka_routes


AsyncRequestHook = Callable[[AsyncContainer], Coroutine[Any, Any, None]]


class AsyncContainerFlask:

    def __init__(
            self,
            app: Flask,
            container: AsyncContainer,
            before_request_hook: Optional[AsyncRequestHook] = None,
    ):
        self.app = app
        self.container = container
        self.before_request_hook = before_request_hook

        self.setup()
        self.verify_routes()

    def setup(self) -> None:
        setup_flask_async_dishka(self.app, self.container, self.before_request_hook)

    def verify_routes(self) -> None:
        verify_dishka_routes(self.app)
