from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.children_organisation import ChildrenOrganisation
from portfolio.models.events import Events


class EventsChild(AbstractModel):
    __tablename__ = "events_child"
    _children_organisation_id = Column(ForeignKey('children_organisation.id', onupdate='CASCADE', ondelete="CASCADE"), type_=Integer, name="children_organisation_id", nullable=False)
    _events_id = Column(ForeignKey('events.id', onupdate='CASCADE', ondelete="CASCADE"), type_=Integer, name="events_id", nullable=False)
    _status = Column(type_=Boolean, name="status", nullable=False, default=False)
    _hours_event = Column(type_=Integer, name="hours_event", nullable=False)
    _children_organisation = relationship("ChildrenOrganisation")
    _events = relationship("Events")
    UniqueConstraint("children_organisation_id", "events_id", name="unique_children_events")

    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 events: Optional[Events] = None,
                 children_organisation: Optional[ChildrenOrganisation] = None,
                 status: Optional[bool] = None) -> None:
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__events = events
        self.__children_organisation = children_organisation
        self.__status = status

    @property
    def events(self) -> Events:
        return self.__events

    @events.setter
    def events(self, value: Events):
        self.__events = value

    @property
    def children_organisation(self) -> ChildrenOrganisation:
        return self.__children_organisation

    @children_organisation.setter
    def children_organisation(self, value: ChildrenOrganisation):
        self.__children_organisation = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value: bool):
        self.__status = value
