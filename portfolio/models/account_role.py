from datetime import datetime
from typing import Optional

import jwt
from sqlalchemy import Column, String

from portfolio.configs.internal import SECRET_KEY, ENCRYPT_ALGORITHM
from portfolio.models.abstract_model import AbstractModel


class AccountRole(AbstractModel):
    __tablename__ = 'account_role'
    _name = Column(name="name", type_=String, nullable=False)

    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 name: Optional[str] = None):
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @staticmethod
    def get_account_role_from_token(token: str):
        if not token:
            return None
        try:
            return int(jwt.decode(token, SECRET_KEY, algorithms=ENCRYPT_ALGORITHM)['account_role_id'])
        except:
            return None
