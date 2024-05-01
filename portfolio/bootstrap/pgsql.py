from drivers.pg_server import Pg
from configs.settings import DB_HOST, DB_USER, DB_PASSWORD, DB_PORT, DB_NAME


def init_pgsql_server():
    Pg.init_db(DB_HOST, DB_USER, DB_PASSWORD, DB_PORT, DB_NAME)
    Pg.init_model()
