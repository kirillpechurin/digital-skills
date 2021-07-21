from typing import Optional, List

from flask import Flask, Blueprint


class FlaskServer:

    _app = Flask(__name__, template_folder='../templates', static_folder='../static')

    @classmethod
    def get_app(cls):
        return cls._app

    @classmethod
    def set_config(cls, secret_key_session: str):
        cls._app.config['SECRET_KEY'] = secret_key_session

    @classmethod
    def set_api(cls, apis: List[Blueprint] or Blueprint):
        for api in apis:
            print(api.name)
            if api.name == 'main':
                cls._app.register_blueprint(api, url_prefix='/')
            else:
                cls._app.register_blueprint(api, url_prefix=f"/{api.name}")

    @classmethod
    def set_rest_api(cls, rest_apis: List[Blueprint] or Blueprint):
        for rest_api in rest_apis:
            print(rest_api.name)
            if rest_api.name == 'main':
                cls._app.register_blueprint(rest_api, url_prefix='/api/')
            else:
                cls._app.register_blueprint(rest_api, url_prefix=f"/api/{rest_api.name}")

    @classmethod
    def run_server(cls, host: str, port: int, debug: bool):
        cls._app.run(
            host=host,
            port=port,
            debug=debug,
            load_dotenv=False
        )
