from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AbstractModel(Base):
    __abstract__ = True
    _id = Column(name="id", type_=Integer, primary_key=True, nullable=False)
    _created_at = Column(name="created_at", type_=DateTime, default=datetime.utcnow, nullable=False)
    _edited_at = Column(name="edited_at", type_=DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None) -> None:
        self.__id = id
        self.__created_at = created_at
        self.__edited_at = edited_at

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int):
        self.__id = value

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @created_at.setter
    def created_at(self, value):
        self.__created_at = value

    @property
    def edited_at(self) -> datetime:
        return self.__edited_at

    @edited_at.setter
    def edited_at(self, value):
        self.__edited_at = value
