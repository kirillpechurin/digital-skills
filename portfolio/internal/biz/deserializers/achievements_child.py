from portfolio.internal.biz.deserializers.achievements import AchievementsDeserializer, \
    DES_FROM_DB_GET_INFO_ACHIEVEMENTS
from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.models.achievements_child import AchievementsChild
from portfolio.models.children_organisation import ChildrenOrganisation
from portfolio.models.organisation import Organisation

DES_FROM_DB_ALL_ACHIEVEMENTS = 'des-from-all-achievements'
DES_FROM_DB_ALL_ACHIEVEMENTS_BY_CHILD_ID = 'des-from-all-achievements-by-child-id'


class AchievementsChildDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_DB_ALL_ACHIEVEMENTS:
            return cls._des_from_db_all_achievements
        elif format_des == DES_FROM_DB_ALL_ACHIEVEMENTS_BY_CHILD_ID:
            return cls._des_from_db_all_achievements_by_child_id
        else:
            raise TypeError

    @staticmethod
    def _des_from_db_all_achievements(data):
        return [
            AchievementsChild(
                id=achievement.get('achievements_child_id'),
                point=achievement.get('achievements_child_point'),
                achievements=AchievementsDeserializer.deserialize(achievement, DES_FROM_DB_GET_INFO_ACHIEVEMENTS),
                children_organisation=ChildrenOrganisation(id=achievement.get('children_organisation_id'))
            )
            for achievement in data
        ]

    @staticmethod
    def _des_from_db_all_achievements_by_child_id(data):
        return [
            AchievementsChild(
                id=achievement.get('achievements_child_id'),
                point=achievement.get('achievements_child_point'),
                achievements=AchievementsDeserializer.deserialize(achievement, DES_FROM_DB_GET_INFO_ACHIEVEMENTS),
                children_organisation=ChildrenOrganisation(
                    organisation=Organisation(id=achievement.get('organisation_id'),
                                              name=achievement.get('organisation_name'))
                )
            )
            for achievement in data
        ]
