import hashlib
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.account_role import AccountRole


class AccountMain(AbstractModel):
    __tablename__ = 'account_main'
    _email = Column(name="email", type_=String(100), unique=True, nullable=False)
    _name = Column(name="name", type_=String(100), nullable=False)
    _hash_password = Column(name="hash_password", type_=String(300), nullable=False)
    _account_role_id = Column(ForeignKey("account_role.id"), name="account_role_id", nullable=False)
    _is_confirmed = Column(name="is_confirmed", type_=Boolean, default=False, nullable=False)
    _account_role = relationship("AccountRole")

    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 email: Optional[str] = None,
                 name: Optional[str] = None,
                 password: Optional[str] = None,
                 hash_password: Optional[str] = None,
                 account_role: Optional[AccountRole] = None,
                 is_confirmed: Optional[bool] = None,
                 is_email_sent: Optional[bool] = None,
                 auth_token: Optional[str] = None):
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__email = email
        self.__name = name
        self.__password = password
        self.__hash_password = hash_password
        self.__account_role = account_role
        self.__is_confirmed = is_confirmed
        self.__is_email_sent = is_email_sent
        self.__auth_token = auth_token

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def name(self) -> str:
        return self.__name

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, value: str):
        self.__password = value

    @property
    def hash_password(self) -> str:
        return self.__hash_password

    @hash_password.setter
    def hash_password(self, value: str):
        self.__hash_password = value

    @property
    def account_role(self):
        return self.__account_role

    @account_role.setter
    def account_role(self, value: AccountRole):
        self.__account_role = value

    @property
    def is_confirmed(self):
        return self.__is_confirmed

    @is_confirmed.setter
    def is_confirmed(self, value: bool):
        self.__is_confirmed = value

    def create_hash_password(self):
        if not self.__password:
            return
        self.__hash_password = hashlib.sha512(bytes(self.__password, 'utf-8')).hexdigest()

    @property
    def is_email_sent(self) -> bool:
        return self.__is_email_sent

    @is_email_sent.setter
    def is_email_sent(self, value: bool):
        self.__is_email_sent = value

    @property
    def auth_token(self) -> str:
        return self.__auth_token

    @auth_token.setter
    def auth_token(self, value):
        self.__auth_token = value
