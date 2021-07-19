from datetime import datetime
from typing import Optional

from sqlalchemy import Column, ForeignKey, Integer, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.achievements import Achievements
from portfolio.models.children_organisation import ChildrenOrganisation


class AchievementsChild(AbstractModel):
    __tablename__ = "achievements_child"
    _children_organisation_id = Column(ForeignKey("children_organisation.id", onupdate="CASCADE", ondelete="CASCADE"), name="children_organisation_id", type_=Integer, nullable=False)
    _achievements_id = Column(ForeignKey("achievements.id", onupdate="CASCADE", ondelete="CASCADE"), name="achievements_id", type_=Integer, nullable=False)
    _point = Column(name="point", type_=Integer, nullable=False)
    UniqueConstraint('point', 'achievements_id', name="unique_point_achievement")
    UniqueConstraint('children_organisation_id', 'achievements_id', name="unique_achievement_for_children")
    _children_organisation = relationship("ChildrenOrganisation")
    _achievements = relationship("Achievements")

    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 children_organisation: Optional[ChildrenOrganisation] = None,
                 point: Optional[int] = None,
                 achievements: Optional[Achievements] = None):
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__children_organisation = children_organisation
        self.__point = point
        self.__achievements = achievements

    @property
    def children_organisation(self):
        return self.__children_organisation

    @property
    def achievements(self):
        return self.__achievements

    @children_organisation.setter
    def children_organisation(self, value: ChildrenOrganisation):
        self.__children_organisation = value

    @achievements.setter
    def achievements(self, value: Achievements):
        self.__achievements = value

    @property
    def point(self):
        return self.__point

    @point.setter
    def point(self, value):
        self.__point = value
