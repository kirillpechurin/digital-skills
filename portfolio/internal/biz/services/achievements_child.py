from portfolio.internal.biz.dao.achievements_child import AchievementsChildDao
from portfolio.models.achievements_child import AchievementsChild


class AchievementsChildService:

    @staticmethod
    def add_achievement(achievements_child: AchievementsChild):
        achievements_child, err = AchievementsChildDao().add_achievement(achievements_child)
        if err:
            return None, err
        return achievements_child, None

    @staticmethod
    def update_by_id(achievements_child: AchievementsChild):
        achievements_child, err = AchievementsChildDao().update(achievements_child.id, achievements_child)
        if err:
            return None, err
        return achievements_child, None

    @staticmethod
    def delete_by_id(achievements_child: AchievementsChild):
        achievements_child, err = AchievementsChildDao().remove_by_id(achievements_child.id)
        if err:
            return None, err
        return achievements_child, None

    @staticmethod
    def get_all_achievements_by_child_id(achievements_child: AchievementsChild):
        achievements_child, err = AchievementsChildDao().get_by_children_id(achievements_child.children_organisation.children.id)
        if err:
            return None, err
        return achievements_child, None
