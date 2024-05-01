from configs.settings import HTTP_HOST, HTTP_PORT, DEBUG, SECRET_KEY_SESSION
from drivers.flask_server import FlaskServer
from internal.http.views.blueprint.api import apis


def init_http_server():
    FlaskServer.set_api(apis)
    FlaskServer.set_config(SECRET_KEY_SESSION)


def run_http_server():
    FlaskServer.run_server(HTTP_HOST, HTTP_PORT, DEBUG)
