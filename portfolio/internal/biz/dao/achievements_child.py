from sqlalchemy import insert, delete

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.achievements_child import AchievementsChildDeserializer, \
    DES_FROM_DB_ALL_ACHIEVEMENTS, DES_FROM_DB_ALL_ACHIEVEMENTS_BY_CHILD_ID
from portfolio.models.achievements import Achievements
from portfolio.models.achievements_child import AchievementsChild
from portfolio.models.children_organisation import ChildrenOrganisation
from portfolio.models.events import Events
from portfolio.models.organisation import Organisation


class AchievementsChildDao(BaseDao):

    def get_by_children_organisation_id(self, children_organisation_id: int):
        with self.session() as sess:
            data = sess.query(
                AchievementsChild._id.label('achievements_child_id'),
                AchievementsChild._point.label('achievements_child_point'),
                Achievements._id.label('achievements_id'),
                Achievements._name.label('achievements_name'),
                Achievements._nomination.label('achievements_nomination'),
                Events._id.label('events_id'),
                Events._name.label('events_name'),
                Events._date_event.label('events_date_event'),
            ).join(
                AchievementsChild._achievements
            ).join(
                AchievementsChild._children_organisation
            ).join(
                Achievements._events
            ).where(
                ChildrenOrganisation._id == children_organisation_id
            ).all()
        if not data:
            return None, None
        data = [dict(row) for row in data]
        return AchievementsChildDeserializer.deserialize(data, DES_FROM_DB_ALL_ACHIEVEMENTS), None

    def get_by_children_id(self, children_id: int):
        with self.session() as sess:
            data = sess.query(
                AchievementsChild._id.label('achievements_child_id'),
                AchievementsChild._point.label('achievements_child_point'),
                Achievements._id.label('achievements_id'),
                Achievements._name.label('achievements_name'),
                Achievements._nomination.label('achievements_nomination'),
                Events._id.label('events_id'),
                Events._name.label('events_name'),
                Events._date_event.label('events_date_event'),
                Organisation._id.label('organisation_id'),
                Organisation._name.label('organisation_name'),
            ).join(
                AchievementsChild._achievements
            ).join(
                AchievementsChild._children_organisation
            ).join(
                Achievements._events
            ).join(
                ChildrenOrganisation._organisation
            ).where(
                ChildrenOrganisation._id == children_id
            ).all()
        if not data:
            return None, None
        data = [dict(row) for row in data]
        return AchievementsChildDeserializer.deserialize(data, DES_FROM_DB_ALL_ACHIEVEMENTS_BY_CHILD_ID), None

    def add_achievement(self, achievements_child: AchievementsChild):
        sql = insert(
            AchievementsChild
        ).values(
            children_organisation_id=achievements_child.children_organisation.id,
            achievements_id=achievements_child.achievements.id,
            point=achievements_child.point,
        ).returning(
            AchievementsChild._id.label('achievements_child_id'),
            AchievementsChild._created_at.label('achievements_child_created_at'),
            AchievementsChild._edited_at.label('achievements_child_edited_at'),
        )
        with self.session() as sess:
            row = sess.execute(sql).first()
            sess.commit()
        row = dict(row)
        achievements_child.id = row['id']
        achievements_child.edited_at = row['edited_at']
        achievements_child.created_at = row['created_at']
        return achievements_child, None

    def update(self, achievements_child_id: int, achievements_child: AchievementsChild):
        with self.session() as sess:
            achievements_child_db = sess.query(AchievementsChild).where(AchievementsChild._id == achievements_child_id)
            achievements_child_db._id = achievements_child.id
            achievements_child_db._point = achievements_child.point
            sess.commit()
        return achievements_child, None

    def remove_by_id(self, achievements_child_id: int):
        sql = delete(
            AchievementsChild
        ).where(AchievementsChild._id == achievements_child_id)
        with self.session() as sess:
            sess.execute(sql)
            sess.commit()
        return achievements_child_id, None
