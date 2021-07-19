from datetime import datetime, date
from typing import Optional

from sqlalchemy import String, Date, Column, ForeignKey, UniqueConstraint, Integer
from sqlalchemy.orm import relationship

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.parents import Parents


class Children(AbstractModel):
    __tablename__ = "children"
    _parents_id = Column(ForeignKey("parents.id", onupdate="CASCADE", ondelete="CASCADE"), type_=Integer, name="parents_id", nullable=False)
    _name = Column(name="name", type_=String, nullable=False)
    _surname = Column(name="surname", type_=String, nullable=False)
    _date_born = Column(name="date_born", type_=Date, nullable=False)
    UniqueConstraint('parents_id', 'name', 'surname', name='unique_children')
    _parents = relationship("Parents")

    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 parents: Optional[Parents] = None,
                 name: Optional[str] = None,
                 surname: Optional[str] = None,
                 date_born: Optional[date] = None) -> None:
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__parents = parents
        self.__name = name
        self.__surname = surname
        self.__date_born = date_born

    @property
    def parents(self) -> Parents:
        return self.__parents

    @parents.setter
    def parents(self, value: Parents):
        self.__parents = value

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
    def surname(self, value):
        self.__surname = value

    @property
    def date_born(self) -> date:
        return self.__date_born

    @date_born.setter
    def date_born(self, value: date):
        self.__date_born = value
