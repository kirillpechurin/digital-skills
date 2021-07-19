from typing import List

from sqlalchemy.orm import sessionmaker

from portfolio.drivers.pg_server import Pg


class BaseDao:

    def __init__(self, sess_transaction=None) -> None:
        self.sess_transaction = sess_transaction
        self.session: sessionmaker = Pg.get_session_db()

    def get_by_id(self, id: int):
        raise NotImplemented

    def add(self, obj: object):
        raise NotImplemented

    def add_many(self, objects: List[object]):
        raise NotImplemented

    def remove(self, obj: object):
        raise NotImplemented

    def remove_by_id(self, id: int):
        raise NotImplemented

    def get_all(self):
        raise NotImplemented

    def update(self, id, obj: object):
        raise NotImplemented

