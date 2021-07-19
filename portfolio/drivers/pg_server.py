from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Pg:

    __engine = None

    @classmethod
    def get_engine(cls):
        return cls.__engine

    @classmethod
    def init_db(cls, host: str, user: str, password: str, port: int, db_name: str):
        cls.__engine = create_engine(f'postgresql://{user}:{password}@{host}/{db_name}')

    @classmethod
    def init_model(cls):
        from portfolio.models import abstract_model, account_main, account_role
        from portfolio.models.abstract_model import Base
        Base.metadata.create_all(cls.__engine)
