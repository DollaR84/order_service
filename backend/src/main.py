import logging

from asgiref.wsgi import WsgiToAsgi

from core.config import Config, get_config
from core.container import setup_container
from presentation import FlaskApp


def get_app() -> WsgiToAsgi:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s  %(process)-7s %(module)-20s %(message)s',
    )

    config: Config = get_config()
    _app = FlaskApp(config)

    container = setup_container(config)
    _app.post_init(container)
    return WsgiToAsgi(_app.app)


app = get_app()
