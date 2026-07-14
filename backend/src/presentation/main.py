from flask import Flask
from dishka import AsyncContainer

from core.di import AsyncContainerFlask
from core.config import Config
from utils.phone import format_phone

from .auth import AuthManager
from .routes import bp_auth, bp_client, bp_order, bp_product, bp_root


class FlaskApp:

    def __init__(self, config: Config):
        self.config = config.flask
        self._app = Flask(
            __name__,
            template_folder=self.config.templates_dir,
            static_folder=self.config.static_dir,
        )

        self._app.config.from_object(self.config)
        self._app.jinja_env.filters["format_phone"] = format_phone

    def post_init(self, container: AsyncContainer) -> None:
        auth = container.get_sync(AuthManager)
        auth.init_app(self._app)

        AsyncContainerFlask(self.app, container)

        self._register_routes()

    def _register_routes(self) -> None:
        self._app.register_blueprint(bp_root)
        self._app.register_blueprint(bp_auth)
        self._app.register_blueprint(bp_client)
        self._app.register_blueprint(bp_order)
        self._app.register_blueprint(bp_product)

    @property
    def app(self) -> Flask:
        return self._app
