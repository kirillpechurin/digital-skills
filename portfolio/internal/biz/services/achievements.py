from typing import List

from portfolio.internal.biz.dao.achievements import AchievementsDao
from portfolio.models.achievements import Achievements
from portfolio.models.events import Events


class AchievementsService:

    @staticmethod
    def get_all_by_completed_events_id(list_completed_events: List[Events]):
        tuple_events_id = tuple([event.events.id for event in list_completed_events]) if list_completed_events else tuple([-1])
        achievements, err = AchievementsDao().get_by_tuple_events_id(tuple_events_id)
        if err:
            return None, err
        return achievements, None

    @staticmethod
    def get_by_events_id(achievements: Achievements):
        list_achievement, err = AchievementsDao().get_by_events_id(achievements.events.id)
        if err:
            return None, err
        return list_achievement, None

    @staticmethod
    def add_achievement(achievement: Achievements):
        achievement, err = AchievementsDao().add(achievement)
        if err:
            return None, err

        return achievement, None

    @staticmethod
    def delete_achievement(achievements: Achievements):
        achievement_id, err = AchievementsDao().remove_by_id(achievements.id)
        if err:
            return None, err
        return achievement_id, None

    @staticmethod
    def edit_achievement(achievements: Achievements):
        achievement, err = AchievementsDao().update(achievements.id, achievements)
        if err:
            return None, err
        return achievement, None

