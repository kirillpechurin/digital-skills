from typing import Tuple

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.achievements import AchievementsDeserializer, DES_FROM_DB_DETAIL_ACHIEVEMENTS
from portfolio.models.achievements import Achievements


class AchievementsDao(BaseDao):

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
        return AchievementsDeserializer.deserialize(data, DES_FROM_DB_DETAIL_ACHIEVEMENTS), None
