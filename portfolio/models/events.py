from datetime import datetime, date
from typing import Optional

from sqlalchemy import Column, String, Date, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.organisation import Organisation


class Events(AbstractModel):
    __tablename__ = 'events'
    _type = Column(type_=String(200), name="type", nullable=False)
    _name = Column(type_=String(200), name="name", nullable=False)
    _date_event = Column(type_=Date, name="date_event", nullable=False)
    _hours = Column(type_=Integer, name="hours", nullable=False)
    _skill = Column(type_=String(200), name="skill", nullable=False)
    _organisation_id = Column(ForeignKey('organisation.id', ondelete="CASCADE", onupdate="CASCADE"), type_=Integer, name="organisation_id", nullable=False)
    _organisation = relationship("Organisation")

    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 type: Optional[str] = None,
                 name: Optional[str] = None,
                 date_event: Optional[date] = None,
                 hours: Optional[int] = None,
                 skill: Optional[str] = None,
                 organisation: Optional[Organisation] = None):
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__type = type
        self.__name = name
        self.__date_event = date_event
        self.__hours = hours
        self.__skill = skill
        self.__organisation = organisation

    @property
    def type(self) -> str:
        return self.__type

    @property
    def name(self) -> str:
        return self.__name

    @property
    def date_event(self) -> date:
        return self.__date_event

    @property
    def hours(self) -> int:
        return self.__hours

    @property
    def skill(self) -> str:
        return self.__skill

    @property
    def organisation(self) -> Organisation:
        return self.__organisation

    @organisation.setter
    def organisation(self, value: Organisation):
        self.__organisation = value
