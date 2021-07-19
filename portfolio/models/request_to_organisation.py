from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Boolean, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.children import Children
from portfolio.models.events import Events
from portfolio.models.parents import Parents


class RequestToOrganisation(AbstractModel):
    __tablename__ = "request_to_organisation"
    _parents_id = Column(ForeignKey("parents.id", ondelete="CASCADE", onupdate="CASCADE"), name="parents_id", type_=Integer, nullable=False)
    _events_id = Column(ForeignKey("events.id", ondelete="CASCADE", onupdate="CASCADE"), name="events_id", type_=Integer, nullable=False)
    _children_id = Column(ForeignKey("children.id", ondelete="CASCADE", onupdate="CASCADE"), name="children_id", type_=Integer, nullable=False)
    _status = Column(name="status", type_=Boolean, nullable=False, default=False)
    _parents = relationship("Parents")
    _events = relationship("Events")
    _children = relationship("Children")
    UniqueConstraint("parents_id", "events_id", "children_id", name='unique_request')

    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 parents: Optional[Parents] = None,
                 events: Optional[Events] = None,
                 children: Optional[Children] = None,
                 status: Optional[bool] = None):
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__parents = parents
        self.__events = events
        self.__children = children
        self.__status = status

    @property
    def parents(self):
        return self.__parents

    @parents.setter
    def parents(self, value: Parents):
        self.__parents = value

    @property
    def events(self):
        return self.__events

    @events.setter
    def events(self, value: Events):
        self.__events = value

    @property
    def children(self):
        return self.__children

    @children.setter
    def children(self, value: Children):
        self.__children = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value: bool):
        self.__status = value