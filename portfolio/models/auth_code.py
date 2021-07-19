from datetime import datetime
from typing import Optional

from portfolio.internal.biz.services.utils import get_random_code
from sqlalchemy import ForeignKey, String, Column, Integer
from sqlalchemy.orm import relationship

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.account_main import AccountMain


class AuthCode(AbstractModel):
    __tablename__ = "auth_code"
    _account_main_id = Column(ForeignKey("account_main.id", onupdate="CASCADE", ondelete="CASCADE"), type_=Integer, name="account_main_id", nullable=False, unique=True)
    _code = Column(name="code", type_=String(6), nullable=False)
    _account_main = relationship("AccountMain")

    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 account_main: Optional[AccountMain] = None,
                 code: Optional[str] = None):
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__account_main = account_main
        self.__code = code

    @property
    def account_main(self) -> AccountMain:
        return self.__account_main

    @property
    def code(self) -> str:
        return self.__code

    def create_random_code(self) -> None:
        self.__code = get_random_code()

    @account_main.setter
    def account_main(self, value):
        self.__account_main = value
