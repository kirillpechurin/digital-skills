from .pgsql import init_pgsql_server
from .servers import init_http_server, run_http_server
from .utils.seeder import seed
from .utils.unpacker import unpack


def setup():
    init_pgsql_server()
    print('[i] Pgsql server inited!')

    print("[i] Unpack data")
    unpack()

    print('[i] Seed database')
    seed()

    print('[i] Success setup!')


def init_all():
    init_http_server()
    print('[i] Http server inited!')

    init_pgsql_server()
    print('[i] Pgsql server inited!')

    print('[i] Http server started...')
    run_http_server()
