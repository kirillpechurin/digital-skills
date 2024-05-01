from internal.biz.deserializers.base_deserializer import BaseDeserializer
from internal.biz.deserializers.events import EventsDeserializer, DES_FROM_DB_INFO_EVENTS
from models.achievements import Achievements

DES_FROM_DB_GET_INFO_ACHIEVEMENTS = 'des-from-db-get-info-achievements'
DES_FROM_DB_ALL_ACHIEVEMENTS = 'des-from-db-all-achievements'
DES_FROM_DB_DETAIL_ACHIEVEMENTS = 'des-from-db-detail-achievements'
DES_FOR_ADD_ACHIEVEMENT = 'des-for-add-achievement'
DES_FOR_EDIT_ACHIEVEMENT = 'des-for-edit-achievement'


class AchievementsDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_DB_GET_INFO_ACHIEVEMENTS:
            return cls._des_from_db_get_info_achievements
        elif format_des == DES_FROM_DB_ALL_ACHIEVEMENTS:
            return cls._des_from_db_all_achievements
        elif format_des == DES_FROM_DB_DETAIL_ACHIEVEMENTS:
            return cls._des_from_db_detail_achievements
        elif format_des == DES_FOR_ADD_ACHIEVEMENT:
            return cls._des_for_add_achievement
        elif format_des == DES_FOR_EDIT_ACHIEVEMENT:
            return cls._des_for_edit_achievement
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

    @staticmethod
    def _des_for_add_achievement(req_form):
        return Achievements(
            name=req_form.get('name'),
            points=[i + 1 for i in range(int(req_form.get('points')))],
            nomination=req_form.get('nomination'),
        )

    @staticmethod
    def _des_for_edit_achievement(req_form):
        return Achievements(
            name=req_form.get('name') if req_form.get('name') else '-1',
            points=[i + 1 for i in range(int(req_form.get('points')))] if req_form.get('points') else [-1],
            nomination=req_form.get('nomination') if req_form.get('nomination') else '-1',
        )