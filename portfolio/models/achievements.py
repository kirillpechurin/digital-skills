from datetime import datetime
from typing import Optional, List

from sqlalchemy import Column, ForeignKey, String, Integer, ARRAY
from sqlalchemy.orm import relationship

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.events import Events


class Achievements(AbstractModel):
    __tablename__ = "achievements"
    _events_id = Column(ForeignKey("events.id", ondelete="CASCADE", onupdate='CASCADE'), name="events_id", type_=Integer, nullable=False)
    _name = Column(name="name", type_=String(200), nullable=False)
    _points = Column(name="points", type_=ARRAY(Integer), nullable=False)
    _nomination = Column(name="nomination", type_=String(150), nullable=False)
    _events = relationship("Events")

    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 events: Optional[Events] = None,
                 name: Optional[str] = None,
                 points: Optional[List] = None,
                 nomination: Optional[str] = None) -> None:
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__events = events
        self.__name = name
        self.__points = points
        self.__nomination = nomination

    @property
    def events(self) -> Events:
        return self.__events

    @events.setter
    def events(self, value: Events):
        self.__events = value

    @property
    def points(self) -> list:
        return self.__points

    @property
    def nomination(self) -> str:
        return self.__nomination

    @property
    def name(self) -> str:
        return self.__name
