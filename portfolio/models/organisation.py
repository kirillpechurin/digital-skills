from datetime import datetime
from typing import Optional

from sqlalchemy import UniqueConstraint, Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.account_main import AccountMain


class Organisation(AbstractModel):
    __tablename__ = "organisation"
    _account_main_id = Column(ForeignKey('account_main.id', onupdate="CASCADE", ondelete='CASCADE'), name="account_main_id", type_=Integer, nullable=False)
    _name = Column(name="name", type_=String(150), nullable=False, )
    _login = Column(name="login", type_=String(50), nullable=False, unique=True)
    _photo_link = Column(name="photo_link", type_=String(500), nullable=True)
    _description = Column(name="description", type_=Text(2000), nullable=True)
    UniqueConstraint("name", "login", name="unique_organisation")
    _account_main = relationship("AccountMain")

    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 account_main: Optional[AccountMain] = None,
                 name: Optional[str] = None,
                 login: Optional[str] = None,
                 photo_link: Optional[str] = None,
                 description: Optional[str] = None):
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__account_main = account_main
        self.__name = name
        self.__login = login
        self.__photo_link = photo_link
        self.__description = description

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
    def login(self) -> str:
        return self.__login

    @property
    def photo_link(self) -> str:
        return self.__photo_link

    @property
    def description(self) -> str:
        return self.__description
