from dishka import from_context, Provider, Scope, provide

from core.config import Config
from presentation import AuthManager


class ApiProvider(Provider):

    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_auth(self, config: Config) -> AuthManager:
        return AuthManager(
            config.admin.username,
            config.admin.password_hash,
            config.admin.secret_key
        )
