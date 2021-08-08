from portfolio.configs.http_server import HOST, PORT, DEBUG, SECRET_KEY_SESSION
from portfolio.drivers.flask_server import FlaskServer
from portfolio.internal.http.views.blueprint.api import apis
from portfolio.internal.http.rest_api.blueprint.rest_api import rest_apis


def init_http_server():
    FlaskServer.set_api(apis)
    FlaskServer.set_rest_api(rest_apis)
    FlaskServer.set_config(SECRET_KEY_SESSION)


def run_http_server():
    FlaskServer.run_server(HOST, PORT, DEBUG)
