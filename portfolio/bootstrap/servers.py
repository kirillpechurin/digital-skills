from portfolio.configs.http_server import HOST, PORT, DEBUG, SECRET_KEY_SESSION
from portfolio.drivers.flask_server import FlaskServer
from portfolio.internal.http.views.blueprint.api import apis


def init_http_server():
    FlaskServer.set_api(apis)
    FlaskServer.set_config(SECRET_KEY_SESSION)


def run_http_server():
    FlaskServer.run_server(HOST, PORT, DEBUG)
