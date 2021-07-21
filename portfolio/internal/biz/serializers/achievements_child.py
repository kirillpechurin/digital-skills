from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.models.achievements_child import AchievementsChild

SER_FOR_DETAIL_ACHIEVEMENT_CHILD = 'ser-for-detail-achievement-child'


class AchievementsChildSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_DETAIL_ACHIEVEMENT_CHILD:
            return cls._ser_for_detail_achievement

    @staticmethod
    def _ser_for_detail_achievement(achievement_child: AchievementsChild):
        return {
            "id": achievement_child.id,
            "point": achievement_child.point,

        }
