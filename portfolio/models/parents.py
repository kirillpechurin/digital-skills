from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Column, Integer, String, UniqueConstraint

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.account_main import AccountMain


class Parents(AbstractModel):
    __tablename__ = "parents"
    _account_main_id = Column(ForeignKey('account_main.id', onupdate="CASCADE", ondelete='CASCADE'), name="account_main_id", type_=Integer, nullable=False)
    _name = Column(name='name', type_=String(150), nullable=False)
    _surname = Column(name='surname', type_=String(150), nullable=False)
    UniqueConstraint("account_main_id", "name", "surname", name='unique_parents')

    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 account_main: Optional[AccountMain] = None,
                 name: Optional[str] = None,
                 surname: Optional[str] = None):
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__account_main = account_main
        self.__name = name
        self.__surname = surname

    @property
    def account_main(self) -> AccountMain:
        return self.__account_main

    @account_main.setter
    def account_main(self, value: AccountMain):
        self.__account_main = value

    @property
    def name(self) -> str:
        return self.__name

    @property
    def surname(self) -> str:
        return self.__surname
