from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.models.achievements import Achievements

SER_FOR_DETAIL_ACHIEVEMENT = 'ser-for-detail-achievement'


class AchievementsSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_DETAIL_ACHIEVEMENT:
            return cls._ser_for_detail_achievement

    @staticmethod
    def _ser_for_detail_achievement(achievement: Achievements):
        return {
            "id": achievement.id,
            "name": achievement.name,
            "points": achievement.points,
            "nomination": achievement.nomination,
        }
