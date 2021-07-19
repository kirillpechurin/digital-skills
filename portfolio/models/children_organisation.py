from datetime import datetime, date
from typing import Optional

from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.children import Children
from portfolio.models.organisation import Organisation


class ChildrenOrganisation(AbstractModel):
    __tablename__ = "children_organisation"
    _organisation_id = Column(ForeignKey("organisation.id", ondelete="CASCADE", onupdate='CASCADE'), type_=Integer, name='organisation_id', nullable="False")
    _children_id = Column(ForeignKey("children.id", onupdate="CASCADE", ondelete='CASCADE'), type_=Integer, name='children_id', nullable=False)
    _organisation = relationship("Organisation")
    _children = relationship("Children")
    UniqueConstraint("children_id", "organisation_id", "unique_children")

    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 organisation: Optional[Organisation] = None,
                 children: Optional[Children] = None):
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__organisation = organisation
        self.__children = children

    @property
    def organisation(self):
        return self.__organisation

    @organisation.setter
    def organisation(self, value: Organisation):
        self.__organisation = value

    @property
    def children(self):
        return self.__children

    @children.setter
    def children(self, value: Children):
        self.__children = value
