import sqlalchemy
from sqlalchemy import insert, delete

from enums.error.errors_enum import ErrorEnum
from internal.biz.dao.base_dao import BaseDao
from internal.biz.deserializers.achievements_child import AchievementsChildDeserializer, \
    DES_FROM_DB_ALL_ACHIEVEMENTS, DES_FROM_DB_ALL_ACHIEVEMENTS_BY_CHILD_ID
from models.achievements import Achievements
from models.achievements_child import AchievementsChild
from models.children_organisation import ChildrenOrganisation
from models.events import Events
from models.organisation import Organisation


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
                ChildrenOrganisation._children_id == children_id
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
            try:
                row = sess.execute(sql).first()
                sess.commit()
                row = dict(row)
            except sqlalchemy.exc.IntegrityError as exception:
                if str(exception.orig)[48:48 + len("unique_point_achievement")] == 'unique_point_achievement':
                    return None, ErrorEnum.unique_point_achievement
                elif str(exception.orig)[48:48 + len('unique_achievement_for_children')] == 'unique_achievement_for_children':
                    return None, ErrorEnum.unique_achievement_for_children
                else:
                    raise TypeError
        achievements_child.id = row['achievements_child_id']
        achievements_child.edited_at = row['achievements_child_created_at']
        achievements_child.created_at = row['achievements_child_edited_at']
        return achievements_child, None

    def update(self, achievements_child_id: int, achievements_child: AchievementsChild):
        with self.session() as sess:
            achievements_child_db = sess.query(AchievementsChild).where(AchievementsChild._id == achievements_child_id).first()
            achievements_child_db._achievements_id = achievements_child.achievements.id
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
