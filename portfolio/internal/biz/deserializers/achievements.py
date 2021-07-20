from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.internal.biz.deserializers.events import EventsDeserializer, DES_FROM_DB_INFO_EVENTS
from portfolio.models.achievements import Achievements

DES_FROM_DB_GET_INFO_ACHIEVEMENTS = 'des-from-db-get-info-achievements'
DES_FROM_DB_ALL_ACHIEVEMENTS = 'des-from-db-all-achievements'
DES_FROM_DB_DETAIL_ACHIEVEMENTS = 'des-from-db-detail-achievements'


class AchievementsDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_DB_GET_INFO_ACHIEVEMENTS:
            return cls._des_from_db_get_info_achievements
        elif format_des == DES_FROM_DB_ALL_ACHIEVEMENTS:
            return cls._des_from_db_all_achievements
        elif format_des == DES_FROM_DB_DETAIL_ACHIEVEMENTS:
            return cls._des_from_db_detail_achievements
        else:
            raise TypeError

    @staticmethod
    def _des_from_db_get_info_achievements(dict_achiev) -> Achievements:
        return Achievements(
            id=dict_achiev.get('achievements_id'),
            name=dict_achiev.get('achievements_name'),
            points=dict_achiev.get('achievements_points'),
            nomination=dict_achiev.get('achievements_nomination'),
            events=EventsDeserializer.deserialize(dict_achiev, DES_FROM_DB_INFO_EVENTS)
        )

    @staticmethod
    def _des_from_db_all_achievements(data):
        return [
            Achievements(
                id=row.get('achievements_id'),
                name=row.get('achievements_name'),
                points=row.get('achievements_points'),
                nomination=row.get('achievements_nomination')
            )
            for row in data
        ]

    @staticmethod
    def _des_from_db_detail_achievements(row):
        return Achievements(
            id=row.get('achievements_id'),
            name=row.get('achievements_name'),
            points=row.get('achievements_points'),
            nomination=row.get('achievements_nomination')
        )
