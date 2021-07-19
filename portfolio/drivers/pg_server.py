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
        import portfolio.models.abstract_model as abc_model
        base = abc_model.Base
        from portfolio.models import \
            account_main, \
            account_role, \
            account_session, \
            achievements, \
            achievements_child, \
            auth_code, \
            children, \
            children_organisation, \
            events, \
            events_child, \
            organisation, \
            parents, \
            employee, \
            request_to_organisation
        base.metadata.create_all(cls.__engine)
