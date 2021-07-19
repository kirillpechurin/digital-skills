import hashlib
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.organisation import Organisation


class Employee(AbstractModel):
    """
    login VARCHAR(150) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    surname VARCHAR(150) NOT NULL,
    specialty VARCHAR(150) NOT NULL,
    organisation_id INTEGER REFERENCES organisation(id) ON DELETE CASCADE
    """
    __tablename__ = "employee"
    _login = Column(name='login', type_=String, nullable=False, unique=True)
    _name = Column(name='name', type_=String, nullable=False)
    _surname = Column(name='surname', type_=String, nullable=False)
    _specialty = Column(name='specialty', type_=String, nullable=False)
    _organisation_id = Column(ForeignKey("organisation.id", ondelete="CASCADE", onupdate="CASCADE"), name='organisation_id', type_=String, nullable=False)
    _organisation = relationship("Organisation")

    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 login: Optional[str] = None,
                 name: Optional[str] = None,
                 surname: Optional[str] = None,
                 specialty: Optional[str] = None,
                 organisation: Optional[Organisation] = None,):
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__login = login
        self.__name = name
        self.__surname = surname
        self.__specialty = specialty
        self.__organisation = organisation

    @property
    def login(self):
        return self.__login

    @login.setter
    def login(self, value: str):
        self.__login = value

    @property
    def organisation(self) -> Organisation:
        return self.__organisation

    @organisation.setter
    def organisation(self, value: Organisation):
        self.__organisation = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def surname(self) -> str:
        return self.__surname

    @surname.setter
    def surname(self, value: str):
        self.__surname = value

    @property
    def specialty(self) -> str:
        return self.__specialty

    @specialty.setter
    def specialty(self, value: str):
        self.__specialty = value
