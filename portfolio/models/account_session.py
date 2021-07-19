from datetime import datetime

import jwt
from sqlalchemy import ForeignKey, Column, Integer
from sqlalchemy.orm import relationship

from portfolio.configs.internal import SECRET_KEY, ENCRYPT_ALGORITHM
from portfolio.models.abstract_model import AbstractModel
from portfolio.models.account_main import AccountMain


class AccountSession(AbstractModel):
    __tablename__ = "account_session"
    _account_main_id = Column(ForeignKey("account_main.id", onupdate="CASCADE", ondelete="CASCADE"), type_=Integer, name="account_main_id", nullable=False)
    _account_main = relationship("AccountMain")

    def __init__(self,
                 id: int = None,
                 created_at: datetime = None,
                 edited_at: datetime = None,
                 account_main: AccountMain = None) -> None:
        super().__init__(id, created_at, edited_at)
        self.__account_main = account_main

    @property
    def account_main(self) -> AccountMain:
        return self.__account_main

    @account_main.setter
    def account_main(self, value: AccountMain):
        self.__account_main = value

    def create_token(self) -> str:
        return jwt.encode(
            {
                'session_id': self.id,
                'account_role_id': self.account_main.account_role.id
            }, SECRET_KEY, algorithm=ENCRYPT_ALGORITHM).decode()

    @staticmethod
    def get_session_id_from_token(token: str):
        if not token:
            return None
        try:
            return int(jwt.decode(token, SECRET_KEY, algorithms=ENCRYPT_ALGORITHM)['session_id'])
        except:
            return None
