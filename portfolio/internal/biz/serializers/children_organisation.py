from typing import List, Dict

from portfolio.internal.biz.serializers.achievements_child import AchievementsChildSerializer, \
    SER_FOR_DETAIL_ACHIEVEMENT_CHILD
from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.internal.biz.serializers.children import ChildrenSerializer, SER_FOR_DETAIL_CHILDREN
from portfolio.internal.biz.serializers.events_child import EventsChildSerializer, SER_FOR_DETAIL_EVENTS_CHILD
from portfolio.models.children_organisation import ChildrenOrganisation

SER_FOR_LIST_LEARNERS = 'ser-for-list-learners'
SER_FOR_DETAIL_LEARNER = 'ser-for-detail-learner'


class ChildrenOrganisationSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_LIST_LEARNERS:
            return cls._ser_for_list_learners
        elif format_ser == SER_FOR_DETAIL_LEARNER:
            return cls._ser_for_detail_learner

    @staticmethod
    def _ser_for_list_learners(list_learners: List[ChildrenOrganisation]):
        return [
            {
                "id": learner.id,
                "children": ChildrenSerializer.serialize(learner.children, SER_FOR_DETAIL_CHILDREN)
            }
            for learner in list_learners
        ]

    @staticmethod
    def _ser_for_detail_learner(dict_for_ser: Dict[str, object or List[object]]):
        return {
            "children_organisation": {
                "id": dict_for_ser.get('children_organisation').id,
                "children": ChildrenSerializer.serialize(dict_for_ser.get('children_organisation').children, SER_FOR_DETAIL_CHILDREN)
            },
            "activity_child": {
                "list_active_events": EventsChildSerializer.serialize(dict_for_ser.get('activity_child').list_active_events, SER_FOR_DETAIL_EVENTS_CHILD),
                "list_completed_event": EventsChildSerializer.serialize(dict_for_ser.get('activity_child').list_completed_events, SER_FOR_DETAIL_EVENTS_CHILD),
                "list_achievements_child": AchievementsChildSerializer.serialize(dict_for_ser.get('activity_child').list_achievements_child, SER_FOR_DETAIL_ACHIEVEMENT_CHILD),
            }
        }
