from typing import Tuple

from sqlalchemy import insert

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.achievements import AchievementsDeserializer, DES_FROM_DB_ALL_ACHIEVEMENTS, DES_FROM_DB_DETAIL_ACHIEVEMENTS
from portfolio.models.achievements import Achievements


class AchievementsDao(BaseDao):

    def add(self, achievement: Achievements):
        sql = insert(
            Achievements
        ).values(
            events_id=achievement.events.id,
            name=achievement.name,
            points=achievement.points,
            nomination=achievement.nomination
        ).returning(
            Achievements._id.label('achievements_id'),
            Achievements._created_at.label('achievements_created_at'),
            Achievements._edited_at.label('achievements_edited_at')
        )
        with self.session() as sess:
            row = sess.execute(sql).first()
            sess.commit()
        achievement.id = row['achievements_id']
        achievement.created_at = row['achievements_created_at']
        achievement.edited_at = row['achievements_edited_at']
        return achievement, None

    def get_by_tuple_events_id(self, tuple_events_id: Tuple[int]):
        with self.session() as sess:
            data = sess.query(
                Achievements._id.label('achievements_id'),
                Achievements._name.label('achievements_name'),
                Achievements._points.label('achievements_points'),
                Achievements._nomination.label('achievements_nomination'),
            ).where(
                Achievements._events_id.in_(tuple_events_id)
            ).all()
        if not data:
            return None, None
        return AchievementsDeserializer.deserialize(data, DES_FROM_DB_ALL_ACHIEVEMENTS), None

    def get_by_events_id(self, events_id: int):
        with self.session() as sess:
            data = sess.query(
                Achievements._id.label('achievements_id'),
                Achievements._name.label('achievements_name'),
                Achievements._points.label('achievements_points'),
                Achievements._nomination.label('achievements_nomination'),
            ).where(
                Achievements._events_id == events_id
            ).first()
        return AchievementsDeserializer.deserialize(data, DES_FROM_DB_DETAIL_ACHIEVEMENTS), None
